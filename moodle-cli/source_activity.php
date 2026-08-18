<?php

function escape_source_activity_html(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function source_activity_minutes(int $minutes): string {
    return $minutes . ($minutes === 1 ? ' minute' : ' minutes');
}

function render_source_activity(array $activity): string {
    $source = $activity['source'];
    $html = '<div class="fx-source-activity">';
    $html .= '<p class="fx-source-activity__purpose">' . escape_source_activity_html($activity['purpose']) . '</p>';
    $html .= '<p><strong>Estimated Activity Duration:</strong> ' . source_activity_minutes($activity['duration_minutes']) . '</p>';
    $html .= '<section aria-labelledby="source-heading"><h3 id="source-heading">Source</h3><dl>';
    $html .= '<dt>Title</dt><dd>' . escape_source_activity_html($source['title']) . '</dd>';
    $html .= '<dt>Publisher</dt><dd>' . escape_source_activity_html($source['publisher']) . '</dd>';
    $html .= '<dt>Type</dt><dd>' . escape_source_activity_html(ucfirst($source['source_type'])) . '</dd>';
    if ($activity['duration_minutes'] !== $source['duration_minutes']) {
        $html .= '<dt>Estimated Source Duration</dt><dd>' . source_activity_minutes($source['duration_minutes']) . '</dd>';
    }
    $html .= '</dl><p><a class="btn btn-primary" href="' . escape_source_activity_html($source['url']) . '" target="_blank" rel="noopener noreferrer">Open Source in a new tab</a></p></section>';
    $html .= '<section aria-labelledby="instructions-heading"><h3 id="instructions-heading">Instructions</h3><p>' . escape_source_activity_html($activity['instructions']) . '</p></section>';
    $html .= '<section aria-labelledby="completion-heading"><h3 id="completion-heading">Completion</h3><p>Finish the Source, produce the result required by the instructions, return to this Course, and select &quot;Mark as done&quot;.</p></section>';
    return $html . '</div>';
}
