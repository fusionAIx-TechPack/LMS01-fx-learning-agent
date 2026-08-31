<?php
// Validates the Course Definition contract on the Moodle side, independently of
// the Python generator. Every generated Course has the same fixed five-activity
// structure; see docs/adr/0004-fixed-four-activity-course-structure.md.

function load_course_definition(string $path): array {
    if (!is_readable($path)) {
        throw new InvalidArgumentException("Course Definition is missing or unreadable: {$path}");
    }
    try {
        $json = file_get_contents($path);
        $document = json_decode($json, false, 512, JSON_THROW_ON_ERROR);
        $definition = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
    } catch (JsonException $error) {
        throw new InvalidArgumentException('Course Definition is not valid JSON: ' . $error->getMessage());
    }
    if (!is_object($document)) {
        throw new InvalidArgumentException('Course Definition must be a JSON object.');
    }

    $text = static function ($value): bool {
        return is_string($value) && trim($value) !== '';
    };
    $positive_int = static function ($value): bool {
        return is_int($value) && $value > 0;
    };
    $http_url = static function ($value): bool {
        return is_string($value)
            && filter_var($value, FILTER_VALIDATE_URL)
            && in_array(parse_url($value, PHP_URL_SCHEME), ['http', 'https'], true);
    };

    $required = [
        'identity.fullname' => $definition['identity']['fullname'] ?? null,
        'identity.shortname' => $definition['identity']['shortname'] ?? null,
        'identity.summary' => $definition['identity']['summary'] ?? null,
    ];
    foreach ($required as $field => $value) {
        if (!$text($value)) {
            throw new InvalidArgumentException("Course Definition requires non-empty {$field}.");
        }
    }
    if (($definition['settings']['format'] ?? null) !== 'topics') {
        throw new InvalidArgumentException('Course Definition settings.format must be "topics".');
    }
    if (($definition['settings']['visible'] ?? null) !== true) {
        throw new InvalidArgumentException('Course Definition settings.visible must be true so the Course is visible when restored.');
    }
    if (($definition['settings']['completion_tracking'] ?? null) !== true) {
        throw new InvalidArgumentException('Course Definition settings.completion_tracking must be true.');
    }
    if (($definition['brief']['language'] ?? null) !== 'en-US') {
        throw new InvalidArgumentException('Course Definition brief.language must be en-US.');
    }
    if (!preg_match('/^[a-z0-9][a-z0-9-]*$/', (string) ($definition['identity']['shortname'] ?? ''))) {
        throw new InvalidArgumentException('Course Definition identity.shortname may contain lowercase letters, numbers, and hyphens only.');
    }
    if (!$positive_int($definition['brief']['learning_time_minutes'] ?? null)) {
        throw new InvalidArgumentException('Course Definition brief.learning_time_minutes must be a positive integer.');
    }
    if (!$http_url($definition['brief']['source_url'] ?? null)) {
        throw new InvalidArgumentException('Course Definition brief.source_url must be a valid HTTP URL.');
    }

    // --- Sources (provenance record) ---------------------------------------
    if (!property_exists($document, 'brief') || !property_exists($document->brief, 'sources')
            || !is_array($document->brief->sources)) {
        throw new InvalidArgumentException('Course Definition brief.sources must be a JSON array.');
    }
    if (empty($definition['brief']['sources'])) {
        throw new InvalidArgumentException('Course Definition requires at least one Source.');
    }
    foreach ($definition['brief']['sources'] as $index => $source) {
        $where = "Course Definition Source {$index}";
        if (!$text($source['title'] ?? null)) {
            throw new InvalidArgumentException("{$where} requires Source title.");
        }
        foreach (['publisher', 'provider_item_id', 'source_type', 'language'] as $field) {
            if (!$text($source[$field] ?? null)) {
                throw new InvalidArgumentException("{$where} requires Source {$field}.");
            }
        }
        if (!in_array($source['source_type'], ['article', 'blog', 'video', 'course'], true)) {
            throw new InvalidArgumentException("{$where} has unsupported Source source_type.");
        }
        if ($source['language'] !== 'en-US') {
            throw new InvalidArgumentException("{$where} Source language must be en-US.");
        }
        if (!$http_url($source['url'] ?? null)) {
            throw new InvalidArgumentException("{$where} requires a valid HTTP Source URL.");
        }
        if (!$positive_int($source['duration_minutes'] ?? null)) {
            throw new InvalidArgumentException("{$where} requires positive Source duration_minutes.");
        }
        if (!$positive_int($source['activity_duration_minutes'] ?? null)
                || $source['activity_duration_minutes'] < $source['duration_minutes']) {
            throw new InvalidArgumentException("{$where} activity_duration_minutes must be at least Source duration_minutes.");
        }
        $access = $source['access'] ?? null;
        if (!is_array($access) || ($access['free'] ?? null) !== true || !$text($access['basis'] ?? null)) {
            throw new InvalidArgumentException("{$where} requires free Source access evidence.");
        }
        if (!$http_url($access['evidence_url'] ?? null)) {
            throw new InvalidArgumentException("{$where} requires a valid HTTP Source access evidence URL.");
        }
        $availability = $source['availability'] ?? null;
        if (!is_array($availability) || !is_int($availability['status'] ?? null)
                || $availability['status'] < 200 || $availability['status'] >= 400
                || !$text($availability['checked_at'] ?? null)) {
            throw new InvalidArgumentException("{$where} requires successful Source availability evidence.");
        }
    }

    // --- Reference videos (optional) --------------------------------------
    if (!property_exists($document->brief, 'reference_videos') || !is_array($document->brief->reference_videos)) {
        throw new InvalidArgumentException('Course Definition brief.reference_videos must be a JSON array.');
    }
    foreach ($definition['brief']['reference_videos'] as $index => $video) {
        $where = "Course Definition reference video {$index}";
        foreach (['title', 'publisher', 'note'] as $field) {
            if (!$text($video[$field] ?? null)) {
                throw new InvalidArgumentException("{$where} requires {$field}.");
            }
        }
        if (!$http_url($video['url'] ?? null)) {
            throw new InvalidArgumentException("{$where} requires a valid HTTP URL.");
        }
        $availability = $video['availability'] ?? null;
        if (!is_array($availability) || !is_int($availability['status'] ?? null)
                || $availability['status'] < 200 || $availability['status'] >= 400
                || !$text($availability['checked_at'] ?? null)) {
            throw new InvalidArgumentException("{$where} requires successful availability evidence.");
        }
    }

    // --- Structure (what the Course is built from) -----------------------
    $structure = $definition['structure'] ?? null;
    if (!is_array($structure)) {
        throw new InvalidArgumentException('Course Definition requires a structure object.');
    }
    foreach (['section_name', 'section_introduction'] as $field) {
        if (!$text($structure[$field] ?? null)) {
            throw new InvalidArgumentException("Course Definition structure.{$field} must be non-empty.");
        }
    }
    $activities = $structure['activities'] ?? null;
    if (!is_array($activities)) {
        throw new InvalidArgumentException('Course Definition structure.activities must be an object.');
    }
    $sourceCount = count($definition['brief']['sources']);
    $videoCount = count($definition['brief']['reference_videos']);

    $overview = $activities['overview'] ?? null;
    if (!is_array($overview) || !$text($overview['name'] ?? null)
            || !$text($overview['instruction'] ?? null) || !$text($overview['outcome'] ?? null)
            || !$text($overview['estimated_time_label'] ?? null)) {
        throw new InvalidArgumentException('Course Definition structure.activities.overview is incomplete.');
    }
    if (($overview['module_count'] ?? null) !== $sourceCount) {
        throw new InvalidArgumentException('Course Definition overview.module_count must equal the number of Sources.');
    }
    if (!$positive_int($overview['estimated_time_minutes'] ?? null)) {
        throw new InvalidArgumentException('Course Definition overview.estimated_time_minutes must be a positive integer.');
    }

    $resources = $activities['resources'] ?? null;
    if (!is_array($resources) || !$text($resources['name'] ?? null) || !$http_url($resources['primary_url'] ?? null)) {
        throw new InvalidArgumentException('Course Definition structure.activities.resources is incomplete.');
    }
    if ($resources['primary_url'] !== $definition['brief']['source_url']) {
        throw new InvalidArgumentException('Course Definition resources.primary_url must be the entered source_url.');
    }

    $videos = $activities['videos'] ?? null;
    if (!is_array($videos) || !$text($videos['name'] ?? null) || !$text($videos['introduction'] ?? null)) {
        throw new InvalidArgumentException('Course Definition structure.activities.videos is incomplete.');
    }
    if (!is_array($videos['items'] ?? null) || count($videos['items']) !== $videoCount) {
        throw new InvalidArgumentException('Course Definition videos.items must match brief.reference_videos.');
    }

    $assignment = $activities['assignment'] ?? null;
    if (!is_array($assignment) || !$text($assignment['name'] ?? null)
            || !$text($assignment['introduction'] ?? null) || !$text($assignment['file_types'] ?? null)) {
        throw new InvalidArgumentException('Course Definition structure.activities.assignment is incomplete.');
    }
    if (!$positive_int($assignment['max_files'] ?? null)) {
        throw new InvalidArgumentException('Course Definition assignment.max_files must be a positive integer.');
    }

    $discussion = $activities['discussion'] ?? null;
    if (!is_array($discussion) || !$text($discussion['name'] ?? null) || !$text($discussion['introduction'] ?? null)) {
        throw new InvalidArgumentException('Course Definition structure.activities.discussion is incomplete.');
    }

    return $definition;
}

function course_html(string $value): string {
    return '<p>' . htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') . '</p>';
}
