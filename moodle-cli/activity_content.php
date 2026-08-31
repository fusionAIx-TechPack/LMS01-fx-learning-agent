<?php
// Renders the learner-visible HTML for each of the five fixed Course activities.
// See docs/adr/0004-fixed-four-activity-course-structure.md.

function fx_esc(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function render_overview_page(array $overview): string {
    $html = '<div class="fx-course-overview">';
    $html .= '<p>' . fx_esc($overview['outcome']) . '</p>';
    $html .= '<ul>';
    $html .= '<li><strong>Number of Modules:</strong> ' . (int) $overview['module_count'] . '</li>';
    $html .= '<li><strong>Estimated Time:</strong> ' . fx_esc($overview['estimated_time_label']) . '</li>';
    $html .= '</ul>';
    $html .= '<p><strong>Instruction:</strong> ' . fx_esc($overview['instruction']) . '</p>';
    return $html . '</div>';
}

function render_videos_page(array $videos): string {
    $html = '<div class="fx-reference-videos">';
    $html .= '<p>' . fx_esc($videos['introduction']) . '</p>';
    if (!empty($videos['items'])) {
        $html .= '<ul>';
        foreach ($videos['items'] as $item) {
            $line = '<a class="nomediaplugin" href="' . fx_esc($item['url'])
                . '" target="_blank" rel="noopener noreferrer">' . fx_esc($item['title']) . '</a>';
            if (!empty($item['note'])) {
                $line .= ' &mdash; ' . fx_esc($item['note']);
            }
            $line .= ' <em>(' . fx_esc((string) $item['publisher']) . ')</em>';
            $html .= '<li>' . $line . '</li>';
        }
        $html .= '</ul>';
    }
    return $html . '</div>';
}

function render_assignment_intro(array $assignment): string {
    return '<div class="fx-course-certification"><p>' . fx_esc($assignment['introduction']) . '</p></div>';
}

function render_discussion_intro(array $discussion): string {
    return '<div class="fx-discussion-forum"><p>' . fx_esc($discussion['introduction']) . '</p></div>';
}
