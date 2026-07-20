// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Script calling into the document through the capability registry.
//!
//! The property under test is not that the operations work — it is that the set
//! script can call and the set an auditor can list are the same set, and that
//! removing one takes effect.

use turing_dom::Dom;
use turing_gc::Bindings;
use turing_html::{Tokenizer, TreeBuilder};
use turing_js::{Host, JsError, Value, Vm, compile};
use turing_webidl::DomHost;

const PAGE: &str = "<html><body>\
     <div id='outer' class='card' data-role='panel'>text <span id='inner'>deep</span></div>\
     </body></html>";

fn dom() -> Dom {
    let tokens = Tokenizer::new(PAGE).tokenize().expect("tokenizes").tokens;
    Dom::new(TreeBuilder::new().build(&tokens).expect("builds"))
}

/// Runs `body` as the whole of `main` against `host`.
fn run(host: &mut dyn Host, body: &str) -> Result<Value, JsError> {
    let program = compile(&format!("function main() {{ {body} }}")).expect("compiles");
    Vm::default().call(&program, "main", Vec::new(), host)
}

// -- the capability surface ----------------------------------------------

#[test]
fn every_listed_operation_is_callable() {
    // One half of the property the registry exists for. An operation that
    // appears in an audit but cannot actually be called makes the listing
    // describe something other than the real surface.
    let dom = dom();
    let mut host = DomHost::new(&dom);
    let listed: Vec<(String, usize)> = host
        .bindings()
        .operations()
        .iter()
        .map(|operation| (operation.name.clone(), operation.arity))
        .collect();
    assert!(!listed.is_empty(), "the default surface is not empty");

    for (name, arity) in listed {
        let arguments = vec!["'outer'"; arity].join(", ");
        let result = run(&mut host, &format!("return {name}({arguments});"));
        assert!(
            !matches!(result, Err(JsError::UnboundOperation { .. })),
            "{name} is listed but not callable"
        );
    }
}

#[test]
fn an_unlisted_operation_is_not_callable() {
    // The other half. `undefined` or a silent no-op would be the tempting
    // outcomes and would both let a typo pass as a call that did nothing.
    let dom = dom();
    let mut host = DomHost::new(&dom);
    assert!(matches!(
        run(&mut host, "return removeEverything('outer');"),
        Err(JsError::UnboundOperation { .. })
    ));
}

#[test]
fn a_revoked_operation_is_refused_on_the_next_call() {
    // The blueprint justifies the registry by grant and revoke, not listing
    // alone. Because invocation resolves through the same table, this needs no
    // second enforcement point that could disagree with the first.
    let dom = dom();
    let mut host = DomHost::new(&dom);
    assert_eq!(
        run(&mut host, "return tagName('outer');").expect("runs"),
        Value::String("div".to_string())
    );

    assert!(host.revoke("tagName"), "the operation was present");

    assert!(matches!(
        run(&mut host, "return tagName('outer');"),
        Err(JsError::UnboundOperation { .. })
    ));
    assert!(
        !host
            .bindings()
            .operations()
            .iter()
            .any(|operation| operation.name == "tagName"),
        "a revoked operation is also gone from the listing"
    );
}

#[test]
fn revoking_something_absent_reports_that_it_was_absent() {
    let dom = dom();
    let mut host = DomHost::new(&dom);
    assert!(!host.revoke("neverRegistered"));
}

#[test]
fn calling_with_the_wrong_argument_count_is_refused() {
    // The registry records arity. Without a check at the call site that record
    // is decorative, and a host indexes past the end of the argument list.
    let dom = dom();
    let mut host = DomHost::new(&dom);
    assert!(matches!(
        run(&mut host, "return getAttribute('outer');"),
        Err(JsError::OperationArity {
            expected: 2,
            got: 1,
            ..
        })
    ));
}

#[test]
fn an_operation_exposed_by_two_interfaces_is_refused() {
    // Script names an operation without naming its interface. Resolving a
    // collision to whichever was registered first hands a script a capability
    // its author did not name, and nothing about that is visible at the call.
    let mut bindings = Bindings::new();
    bindings.register("Document", "shared", 0);
    bindings.register("Element", "shared", 0);
    assert!(bindings.resolve_global("shared").is_err());
    assert!(bindings.resolve_global("absent").is_err());

    bindings.register("Document", "unique", 0);
    assert_eq!(
        bindings
            .resolve_global("unique")
            .expect("resolves")
            .interface,
        "Document"
    );
}

// -- the operations ------------------------------------------------------

#[test]
fn script_reads_the_document_through_bound_operations() {
    let dom = dom();
    let mut host = DomHost::new(&dom);

    assert_eq!(
        run(&mut host, "return tagName('outer');").expect("runs"),
        Value::String("div".to_string())
    );
    assert_eq!(
        run(&mut host, "return getAttribute('outer', 'class');").expect("runs"),
        Value::String("card".to_string())
    );
    assert_eq!(
        run(&mut host, "return hasElement('inner');").expect("runs"),
        Value::Boolean(true)
    );
    assert_eq!(
        run(&mut host, "return hasElement('missing');").expect("runs"),
        Value::Boolean(false)
    );
}

#[test]
fn a_missing_attribute_is_null_rather_than_undefined() {
    // The DOM specifies null. `undefined` is the natural guess here and is a
    // different value that script can distinguish.
    let dom = dom();
    let mut host = DomHost::new(&dom);
    assert_eq!(
        run(&mut host, "return getAttribute('outer', 'nope');").expect("runs"),
        Value::Null
    );
}

#[test]
fn text_content_reads_descendants_in_document_order() {
    let dom = dom();
    let mut host = DomHost::new(&dom);
    assert_eq!(
        run(&mut host, "return textContent('outer');").expect("runs"),
        Value::String("text deep".to_string())
    );
}

#[test]
fn an_operation_on_a_missing_element_fails_with_a_reason() {
    // Not `undefined`, and not an empty string: the script asked about
    // something that is not there, and that is worth saying.
    let dom = dom();
    let mut host = DomHost::new(&dom);
    let result = run(&mut host, "return tagName('missing');");
    match result {
        Err(JsError::HostOperationFailed { message, .. }) => {
            assert!(message.contains("missing"), "the message names the id");
        }
        other => panic!("expected a host failure, got {other:?}"),
    }
}

// -- interaction with script ---------------------------------------------

#[test]
fn a_script_function_wins_a_name_collision() {
    // A program's own declaration must not be shadowed by whatever the embedder
    // happens to expose, or adding a binding could silently change the meaning
    // of an existing script.
    let dom = dom();
    let mut host = DomHost::new(&dom);
    let program = compile(
        "function tagName(id) { return 'shadowed'; } \
         function main() { return tagName('outer'); }",
    )
    .expect("compiles");

    assert_eq!(
        Vm::default()
            .call(&program, "main", Vec::new(), &mut host)
            .expect("runs"),
        Value::String("shadowed".to_string())
    );
}

#[test]
fn a_run_with_no_host_refuses_every_operation() {
    // The default. A script that calls out when nothing is bound must fail
    // rather than the absence of a host being a special case somewhere.
    let program = compile("function main() { return tagName('outer'); }").expect("compiles");
    assert!(matches!(
        Vm::default().call(
            &program,
            "main",
            Vec::new(),
            &mut turing_js::NoHost::default()
        ),
        Err(JsError::UnboundOperation { .. })
    ));
}
