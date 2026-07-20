// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Accessibility tree tests.
//!
//! Every case here is one where a wrong implementation is quiet: it produces a
//! tree that reads correctly to anyone inspecting it and is wrong to anyone
//! using an assistive technology.
//!
//! The foreign-tree module is not gated on the `html` feature, so it also runs
//! in the zero-dependency configuration an embedder builds.

use turing_a11y::{Role, SemanticTree, build};
use turing_css::ElementTree;

// -- a document the engine does not own ----------------------------------

struct HostNode {
    tag: Option<String>,
    text: Option<String>,
    id: Option<String>,
    label: Option<String>,
    parent: Option<usize>,
    children: Vec<usize>,
}

struct HostTree {
    nodes: Vec<HostNode>,
}

impl ElementTree for HostTree {
    type Node = usize;

    fn is_element(&self, node: Self::Node) -> bool {
        self.nodes[node].tag.is_some()
    }

    fn tag_name(&self, node: Self::Node) -> Option<&str> {
        self.nodes[node].tag.as_deref()
    }

    fn attribute(&self, node: Self::Node, name: &str) -> Option<&str> {
        match name {
            "id" => self.nodes[node].id.as_deref(),
            "aria-label" => self.nodes[node].label.as_deref(),
            _ => None,
        }
    }

    fn parent(&self, node: Self::Node) -> Option<Self::Node> {
        self.nodes[node].parent
    }

    fn previous_element_sibling(&self, node: Self::Node) -> Option<Self::Node> {
        let parent = self.nodes[node].parent?;
        let siblings = &self.nodes[parent].children;
        let position = siblings.iter().position(|&s| s == node)?;
        siblings[..position]
            .iter()
            .rev()
            .copied()
            .find(|&s| self.is_element(s))
    }
}

impl SemanticTree for HostTree {
    fn root(&self) -> Self::Node {
        0
    }

    fn children(&self, node: Self::Node) -> Vec<Self::Node> {
        self.nodes[node].children.clone()
    }

    fn text(&self, node: Self::Node) -> Option<&str> {
        self.nodes[node].text.as_deref()
    }

    fn element_by_id(&self, id: &str) -> Option<Self::Node> {
        self.nodes.iter().position(|n| n.id.as_deref() == Some(id))
    }

    fn node_index(&self, node: Self::Node) -> usize {
        node
    }
}

/// Builds `<root><div><h1>Title</h1><button aria-label="Go"/></div></root>`.
fn host_sample() -> HostTree {
    let element = |tag: &str, parent: usize, children: Vec<usize>, label: Option<&str>| HostNode {
        tag: Some(tag.to_string()),
        text: None,
        id: None,
        label: label.map(str::to_string),
        parent: Some(parent),
        children,
    };
    HostTree {
        nodes: vec![
            HostNode {
                tag: None,
                text: None,
                id: None,
                label: None,
                parent: None,
                children: vec![1],
            },
            element("div", 0, vec![2, 4], None),
            element("h1", 1, vec![3], None),
            HostNode {
                tag: None,
                text: Some("Title".to_string()),
                id: None,
                label: None,
                parent: Some(2),
                children: Vec::new(),
            },
            element("button", 1, Vec::new(), Some("Go")),
        ],
    }
}

#[test]
fn builds_from_a_tree_the_engine_does_not_own() {
    let tree = build(&host_sample()).expect("builds");
    let div = &tree.children[0];
    assert_eq!(div.role, Role::Generic);

    let heading = &div.children[0];
    assert_eq!(heading.role, Role::Heading { level: 1 });
    assert_eq!(heading.name.as_deref(), Some("Title"));

    let button = &div.children[1];
    assert_eq!(button.role, Role::Button);
    assert_eq!(button.name.as_deref(), Some("Go"));
}

// -- the engine's own document -------------------------------------------

#[cfg(feature = "html")]
mod html {
    use super::{Role, build};
    use turing_a11y::{A11yError, AccessibilityNode};
    use turing_html::{Document, Tokenizer, TreeBuilder};

    fn document(html: &str) -> Document {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        TreeBuilder::new().build(&tokens).expect("builds")
    }

    fn tree(html: &str) -> Result<AccessibilityNode, A11yError> {
        build(&document(html))
    }

    /// Returns every node of `role`, in tree order.
    fn all_with_role(node: &AccessibilityNode, role: &Role) -> Vec<AccessibilityNode> {
        let mut found = Vec::new();
        if node.role == *role {
            found.push(node.clone());
        }
        for child in &node.children {
            found.extend(all_with_role(child, role));
        }
        found
    }

    fn only(node: &AccessibilityNode, role: &Role) -> AccessibilityNode {
        let found = all_with_role(node, role);
        assert_eq!(found.len(), 1, "expected exactly one {role:?}");
        found.into_iter().next().expect("checked above")
    }

    // -- roles -----------------------------------------------------------

    #[test]
    fn maps_implicit_roles_from_the_host_language() {
        let root =
            tree("<html><body><nav><ul><li><a href='/x'>Home</a></li></ul></nav></body></html>")
                .expect("builds");
        assert_eq!(all_with_role(&root, &Role::Navigation).len(), 1);
        assert_eq!(all_with_role(&root, &Role::List).len(), 1);
        assert_eq!(all_with_role(&root, &Role::ListItem).len(), 1);
        assert_eq!(all_with_role(&root, &Role::Link).len(), 1);
    }

    #[test]
    fn an_anchor_without_href_is_not_a_link() {
        // Announcing it as a link offers an action that does not exist.
        let root = tree("<html><body><a>text</a></body></html>").expect("builds");
        assert!(all_with_role(&root, &Role::Link).is_empty());
        assert_eq!(all_with_role(&root, &Role::Generic).len(), 1);
    }

    #[test]
    fn an_explicit_role_overrides_the_implicit_one() {
        let root = tree("<html><body><div role='button'>Go</div></body></html>").expect("builds");
        let button = only(&root, &Role::Button);
        assert_eq!(button.name.as_deref(), Some("Go"));
    }

    #[test]
    fn a_header_in_the_body_is_a_banner() {
        let root = tree("<html><body><header>Site</header></body></html>").expect("builds");
        assert_eq!(all_with_role(&root, &Role::Banner).len(), 1);
    }

    #[test]
    fn a_header_inside_a_sectioning_element_is_not_a_banner() {
        // Exposing a per-section header as the page banner would put a landmark
        // on every entry in a feed. Omitting the scoping rule still produces a
        // tree that looks entirely reasonable.
        let root =
            tree("<html><body><nav><header>Menu</header></nav></body></html>").expect("builds");
        assert!(all_with_role(&root, &Role::Banner).is_empty());
        assert_eq!(all_with_role(&root, &Role::Navigation).len(), 1);
    }

    #[test]
    fn a_footer_in_the_body_is_contentinfo() {
        let root = tree("<html><body><footer>Legal</footer></body></html>").expect("builds");
        assert_eq!(all_with_role(&root, &Role::ContentInfo).len(), 1);
    }

    #[test]
    fn an_unmapped_element_is_reported_not_guessed() {
        // `<section>` maps to `region`, but only when it has an accessible
        // name, and to `generic` otherwise. That conditional is not modelled,
        // so the element is refused rather than assigned either one.
        //
        // `<table>` would be the more obvious case and cannot be used: the tree
        // builder refuses table construction before this crate ever sees it.
        let result = tree("<html><body><section>x</section></body></html>");
        assert!(matches!(
            result,
            Err(A11yError::ElementNotMapped { ref tag }) if tag == "section"
        ));
    }

    #[test]
    fn an_unmodelled_role_token_is_reported_not_guessed() {
        // ARIA specifies falling back to the implicit role for an *invalid*
        // token, but this implementation cannot distinguish an invalid token
        // from a valid one it has not modelled, and silently treating
        // role='tablist' as a div reads as correct.
        let result = tree("<html><body><div role='tablist'></div></body></html>");
        assert!(matches!(
            result,
            Err(A11yError::RoleUnsupported { ref role }) if role == "tablist"
        ));
    }

    #[test]
    fn heading_levels_are_preserved() {
        let root = tree("<html><body><h1>a</h1><h3>b</h3></body></html>").expect("builds");
        assert_eq!(all_with_role(&root, &Role::Heading { level: 1 }).len(), 1);
        assert_eq!(all_with_role(&root, &Role::Heading { level: 3 }).len(), 1);
        assert!(all_with_role(&root, &Role::Heading { level: 2 }).is_empty());
    }

    #[test]
    fn document_structure_elements_do_not_appear_in_the_tree() {
        let root = tree("<html><head><title>T</title></head><body><p>x</p></body></html>")
            .expect("builds");
        assert_eq!(root.role, Role::Document);
        assert_eq!(
            root.children.len(),
            1,
            "html, head, body, title are absorbed"
        );
        assert_eq!(root.children[0].role, Role::Paragraph);
    }

    // -- hidden and presentational ---------------------------------------

    #[test]
    fn aria_hidden_removes_the_element_and_its_subtree() {
        let root = tree(
            "<html><body><div aria-hidden='true'><h1>Gone</h1></div><h2>Kept</h2></body></html>",
        )
        .expect("builds");
        assert!(all_with_role(&root, &Role::Heading { level: 1 }).is_empty());
        assert_eq!(all_with_role(&root, &Role::Heading { level: 2 }).len(), 1);
    }

    #[test]
    fn presentation_strips_the_element_but_keeps_its_children() {
        // The opposite direction from aria-hidden. Conflating the two either
        // over-exposes hidden content or hides real content, and both produce a
        // tree that looks fine until someone uses a screen reader.
        let root = tree("<html><body><ul role='presentation'><li>Item</li></ul></body></html>")
            .expect("builds");
        assert!(
            all_with_role(&root, &Role::List).is_empty(),
            "the list itself is stripped"
        );
        assert_eq!(
            all_with_role(&root, &Role::ListItem).len(),
            1,
            "its children stay exposed"
        );
    }

    #[test]
    fn none_is_a_synonym_for_presentation() {
        let root =
            tree("<html><body><ul role='none'><li>Item</li></ul></body></html>").expect("builds");
        assert!(all_with_role(&root, &Role::List).is_empty());
        assert_eq!(all_with_role(&root, &Role::ListItem).len(), 1);
    }

    #[test]
    fn an_image_with_empty_alt_is_decorative_and_not_exposed() {
        let root = tree("<html><body><img alt=''><img alt='Chart'></body></html>").expect("builds");
        let images = all_with_role(&root, &Role::Image);
        assert_eq!(images.len(), 1);
        assert_eq!(images[0].name.as_deref(), Some("Chart"));
    }

    // -- accessible name precedence --------------------------------------

    #[test]
    fn labelledby_wins_over_every_lower_source() {
        // Every lower rung is present at once. An implementation that checks
        // them in the wrong order still yields a plausible name, so a test
        // supplying one source at a time would not catch it.
        let root = tree(
            "<html><body><span id='lbl'>From labelledby</span>\
             <button aria-labelledby='lbl' aria-label='From label' title='From title'>\
             From content</button></body></html>",
        )
        .expect("builds");
        assert_eq!(
            only(&root, &Role::Button).name.as_deref(),
            Some("From labelledby")
        );
    }

    #[test]
    fn aria_label_wins_over_content_and_title() {
        let root = tree(
            "<html><body><button aria-label='From label' title='From title'>\
             From content</button></body></html>",
        )
        .expect("builds");
        assert_eq!(
            only(&root, &Role::Button).name.as_deref(),
            Some("From label")
        );
    }

    #[test]
    fn content_wins_over_title_for_a_role_that_names_from_content() {
        let root =
            tree("<html><body><button title='From title'>From content</button></body></html>")
                .expect("builds");
        assert_eq!(
            only(&root, &Role::Button).name.as_deref(),
            Some("From content")
        );
    }

    #[test]
    fn title_is_used_only_when_nothing_else_names_the_element() {
        let root =
            tree("<html><body><button title='From title'></button></body></html>").expect("builds");
        assert_eq!(
            only(&root, &Role::Button).name.as_deref(),
            Some("From title")
        );
    }

    #[test]
    fn a_role_that_does_not_name_from_content_ignores_its_text() {
        // A paragraph is not named by its own prose. Concatenating descendant
        // text for every role is the classic quiet defect here: it reads
        // plausibly and gives a text box the name of whatever sits inside it.
        let root = tree("<html><body><p>Some prose</p></body></html>").expect("builds");
        assert_eq!(only(&root, &Role::Paragraph).name, None);
    }

    #[test]
    fn labelledby_concatenates_multiple_references_in_order() {
        let root = tree(
            "<html><body><span id='a'>First</span><span id='b'>Second</span>\
             <button aria-labelledby='a b'></button></body></html>",
        )
        .expect("builds");
        assert_eq!(
            only(&root, &Role::Button).name.as_deref(),
            Some("First Second")
        );
    }

    #[test]
    fn a_labelledby_reference_to_a_missing_element_is_ignored() {
        // Specified behaviour: an authoring error, not an engine error.
        let root = tree(
            "<html><body><span id='a'>First</span>\
             <button aria-labelledby='a missing'></button></body></html>",
        )
        .expect("builds");
        assert_eq!(only(&root, &Role::Button).name.as_deref(), Some("First"));
    }

    #[test]
    fn a_labelledby_cycle_terminates() {
        // Without a visited set threaded through the recursion this exhausts
        // the stack, which is a denial of service reachable from ordinary page
        // content. The test fails by crashing rather than by asserting.
        let root = tree(
            "<html><body>\
             <button id='one' aria-labelledby='two'>One</button>\
             <button id='two' aria-labelledby='one'>Two</button>\
             </body></html>",
        )
        .expect("builds");
        assert_eq!(all_with_role(&root, &Role::Button).len(), 2);
    }

    #[test]
    fn an_element_labelled_by_itself_terminates() {
        let root =
            tree("<html><body><button id='me' aria-labelledby='me'>Text</button></body></html>")
                .expect("builds");
        // The self-reference is skipped, so the name falls through to content.
        assert_eq!(only(&root, &Role::Button).name.as_deref(), Some("Text"));
    }

    #[test]
    fn a_hidden_subtree_contributes_nothing_to_a_name() {
        let root = tree(
            "<html><body><button>Visible<span aria-hidden='true'>Hidden</span></button>\
             </body></html>",
        )
        .expect("builds");
        assert_eq!(only(&root, &Role::Button).name.as_deref(), Some("Visible"));
    }

    // -- controls --------------------------------------------------------

    #[test]
    fn an_input_without_an_aria_name_is_reported_not_assumed_unnamed() {
        // A <label for> elsewhere in the document is the usual way a control is
        // named. Reporting the control as unnamed would hide a named control
        // behind a missing feature, and those are very different findings.
        let result = tree("<html><body><input type='text'></body></html>");
        assert!(matches!(
            result,
            Err(A11yError::NameSourceUnsupported { ref tag, .. }) if tag == "input"
        ));
    }

    #[test]
    fn an_input_with_an_aria_label_is_named() {
        let root = tree("<html><body><input type='text' aria-label='Search'></body></html>")
            .expect("builds");
        assert_eq!(only(&root, &Role::Textbox).name.as_deref(), Some("Search"));
    }

    #[test]
    fn an_input_defaults_to_a_textbox_when_type_is_absent() {
        let root = tree("<html><body><input aria-label='Search'></body></html>").expect("builds");
        assert_eq!(all_with_role(&root, &Role::Textbox).len(), 1);
    }

    #[test]
    fn an_unmodelled_input_type_is_reported() {
        let result = tree("<html><body><input type='range' aria-label='x'></body></html>");
        assert!(matches!(result, Err(A11yError::RoleUnsupported { .. })));
    }

    #[test]
    fn a_checkbox_input_maps_to_the_checkbox_role() {
        let root = tree("<html><body><input type='checkbox' aria-label='Agree'></body></html>")
            .expect("builds");
        assert_eq!(only(&root, &Role::Checkbox).name.as_deref(), Some("Agree"));
    }
}
