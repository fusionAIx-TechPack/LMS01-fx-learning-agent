<?php
const MAX_NAVIGATION_NAME_LENGTH = 40;

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
    $required = [
        'identity.fullname' => $definition['identity']['fullname'] ?? null,
        'identity.shortname' => $definition['identity']['shortname'] ?? null,
        'identity.summary' => $definition['identity']['summary'] ?? null,
        'general.name' => $definition['general']['name'] ?? null,
        'general.introduction' => $definition['general']['introduction'] ?? null,
    ];
    foreach ($required as $field => $value) {
        if (!is_string($value) || trim($value) === '') {
            throw new InvalidArgumentException("Course Definition requires non-empty {$field}.");
        }
    }
    if (($definition['settings']['format'] ?? null) !== 'topics') {
        throw new InvalidArgumentException('Course Definition settings.format must be "topics".');
    }
    if (($definition['settings']['visible'] ?? null) !== false) {
        throw new InvalidArgumentException('Course Definition settings.visible must be false for review.');
    }
    if (($definition['settings']['completion_tracking'] ?? null) !== true) {
        throw new InvalidArgumentException('Course Definition settings.completion_tracking must be true.');
    }
    if (($definition['brief']['language'] ?? null) !== 'en-US') {
        throw new InvalidArgumentException('Course Definition brief.language must be en-US.');
    }
    if (!preg_match('/^[a-z0-9][a-z0-9-]*$/', $definition['identity']['shortname'])) {
        throw new InvalidArgumentException('Course Definition identity.shortname may contain lowercase letters, numbers, and hyphens only.');
    }
    if (!property_exists($document, 'modules') || !is_array($document->modules)) {
        throw new InvalidArgumentException('Course Definition modules must be a JSON array.');
    }
    if (empty($definition['modules'])) {
        throw new InvalidArgumentException('Course Definition requires at least one module.');
    }
    $purposes = [];
    $instructions = [];
    foreach ($definition['modules'] as $moduleIndex => $module) {
        foreach (['name', 'introduction'] as $field) {
            if (!is_string($module[$field] ?? null) || trim($module[$field]) === '') {
                throw new InvalidArgumentException("Course Definition module {$moduleIndex} requires non-empty {$field}.");
            }
        }
        if (mb_strlen($module['name']) > MAX_NAVIGATION_NAME_LENGTH) {
            throw new InvalidArgumentException("Course Definition module {$moduleIndex} name must be at most " . MAX_NAVIGATION_NAME_LENGTH . ' characters for Moodle navigation.');
        }
        $moduleDocument = $document->modules[$moduleIndex] ?? null;
        if (!is_object($moduleDocument) || !property_exists($moduleDocument, 'activities') || !is_array($moduleDocument->activities)) {
            throw new InvalidArgumentException("Course Definition module {$moduleIndex} activities must be a JSON array.");
        }
        if (empty($module['activities'])) {
            throw new InvalidArgumentException("Course Definition module {$moduleIndex} requires at least one Learning Activity.");
        }
        foreach ($module['activities'] as $activityIndex => $activity) {
            foreach (['name', 'purpose', 'instructions'] as $field) {
                if (!is_string($activity[$field] ?? null) || trim($activity[$field]) === '') {
                    throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires non-empty {$field}.");
                }
            }
            if (in_array($activity['purpose'], $purposes, true)) {
                throw new InvalidArgumentException('Source Activity purpose must be unique within the Course.');
            }
            $purposes[] = $activity['purpose'];
            if (in_array($activity['instructions'], $instructions, true)) {
                throw new InvalidArgumentException('Source Activity instructions must be unique within the Course.');
            }
            $instructions[] = $activity['instructions'];
            if (mb_strlen($activity['name']) > MAX_NAVIGATION_NAME_LENGTH) {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} name must be at most " . MAX_NAVIGATION_NAME_LENGTH . ' characters for Moodle navigation.');
            }
            if (!is_int($activity['duration_minutes'] ?? null) || $activity['duration_minutes'] <= 0) {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires positive duration_minutes.");
            }
            if (!is_string($activity['source']['title'] ?? null) || trim($activity['source']['title']) === '') {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires Source title.");
            }
            foreach (['publisher', 'provider_item_id', 'source_type', 'language'] as $field) {
                if (!is_string($activity['source'][$field] ?? null) || trim($activity['source'][$field]) === '') {
                    throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires Source {$field}.");
                }
            }
            if (!in_array($activity['source']['source_type'], ['article', 'blog', 'video', 'course'], true)) {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} has unsupported Source source_type.");
            }
            if (!is_int($activity['source']['duration_minutes'] ?? null) || $activity['source']['duration_minutes'] <= 0) {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires positive Source duration_minutes.");
            }
            if ($activity['duration_minutes'] < $activity['source']['duration_minutes']) {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} duration_minutes must be at least Source duration_minutes.");
            }
            if ($activity['source']['language'] !== 'en-US') {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} Source language must be en-US.");
            }
            $url = $activity['source']['url'] ?? null;
            if (!is_string($url) || !filter_var($url, FILTER_VALIDATE_URL) || !in_array(parse_url($url, PHP_URL_SCHEME), ['http', 'https'], true)) {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires a valid HTTP Source URL.");
            }
            $access = $activity['source']['access'] ?? null;
            if (!is_array($access) || ($access['free'] ?? null) !== true) {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires free Source access evidence.");
            }
            if (!is_string($access['basis'] ?? null) || trim($access['basis']) === '') {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires Source access basis.");
            }
            $evidenceUrl = $access['evidence_url'] ?? null;
            if (!is_string($evidenceUrl) || !filter_var($evidenceUrl, FILTER_VALIDATE_URL) || !in_array(parse_url($evidenceUrl, PHP_URL_SCHEME), ['http', 'https'], true)) {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires a valid HTTP Source access evidence URL.");
            }
            $availability = $activity['source']['availability'] ?? null;
            if (!is_array($availability) || !is_int($availability['status'] ?? null)
                    || $availability['status'] < 200 || $availability['status'] >= 400
                    || !is_string($availability['checked_at'] ?? null) || trim($availability['checked_at']) === '') {
                throw new InvalidArgumentException("Learning Activity {$moduleIndex}.{$activityIndex} requires successful Source availability evidence.");
            }
        }
    }
    return $definition;
}

function course_html(string $value): string {
    return '<p>' . htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') . '</p>';
}
