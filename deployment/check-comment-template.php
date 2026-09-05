<?php
// Exercise the real theme expression with a percent-encoded Chinese permalink.
$source = file_get_contents($argv[1]);
$start = strpos($source, "'submit_button'");
$end = strpos($source, "'comment_notes_after'", $start);
if ($start === false || $end === false) {
    throw new RuntimeException('Comment submit template was not found');
}
$expression = substr($source, $start, $end - $start);
$expression = substr($expression, strpos($expression, '=>') + 2);
$expression = rtrim(trim($expression), ',');
function iro_opt($key) { return 'Send 100%'; }
function esc_attr($value) { return htmlspecialchars($value, ENT_QUOTES); }
function wp_nonce_field(...$args) {
    return '<input name="_wp_http_referer" value="/2026/%e6%ad%a5/?next=50%25">';
}
$smilies_button = '<span>50%</span>';
$img_upload = '';
$template = eval('return ' . $expression . ';');
$rendered = sprintf($template, 'submit', 'submit', 'submit', 'Send');
foreach (['Send 100%', '50%', '/2026/%e6%ad%a5/?next=50%25'] as $literal) {
    if (!str_contains($rendered, $literal)) {
        throw new RuntimeException('Literal text changed: ' . $literal);
    }
}
echo "Comment template preserves percent-encoded URLs and literal labels\n";
