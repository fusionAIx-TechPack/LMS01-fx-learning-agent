<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/completionlib.php');
require_once(__DIR__ . '/course_definition.php');
function assert_course(bool $condition, string $message): void {
    if (!$condition) throw new RuntimeException($message);
}
$definition = load_course_definition($argv[1] ?? '');
$course = $DB->get_record('course', ['shortname' => $definition['identity']['shortname']], '*', MUST_EXIST);
$mode = $argv[2] ?? 'structure';
if ($mode === 'completion-incomplete' || $mode === 'completion-complete') {
    $userid = filter_var($argv[3] ?? null, FILTER_VALIDATE_INT);
    assert_course($userid !== false && $userid > 0, 'Completion verification requires a valid learner user ID.');
    $firstLearningActivityModule = array_values($DB->get_records('course_modules', ['course' => $course->id], 'id'))[0] ?? null;
    assert_course($firstLearningActivityModule !== null, 'Course has no learner-visible Learning Activity.');
    $completion = new completion_info($course);
    $cm = get_coursemodule_from_id('page', $firstLearningActivityModule->id, $course->id, false, MUST_EXIST);
    $state = $completion->get_data($cm, false, $userid);
    if ($mode === 'completion-incomplete') {
        assert_course($state->completionstate == COMPLETION_INCOMPLETE, 'The Learning Activity was completed without learner confirmation.');
        echo "Verified that opening the learner-visible Source does not complete the Learning Activity.\n";
    } else {
        assert_course($state->completionstate == COMPLETION_COMPLETE, 'The learner confirmation did not complete the Learning Activity.');
        echo "Verified explicit learner completion confirmation.\n";
    }
    exit(0);
}
assert_course($course->fullname === $definition['identity']['fullname'], 'Course identity was not preserved.');
assert_course($course->visible == 0, 'Restored Course must remain hidden.');
assert_course($course->format === 'topics', 'Restored Course must use topic format.');
assert_course($course->enablecompletion == 1, 'Course completion tracking must be enabled.');
$sections = array_values($DB->get_records('course_sections', ['course' => $course->id], 'section'));
assert_course(count($sections) === count($definition['modules']) + 1, 'Course module structure was not preserved.');
assert_course($sections[0]->name === $definition['general']['name'], 'General section was not preserved.');
$expectedActivities = [];
foreach ($definition['modules'] as $moduleIndex => $moduleDefinition) {
    $section = $sections[$moduleIndex + 1] ?? null;
    assert_course($section && $section->name === $moduleDefinition['name'], "Module {$moduleIndex} was not preserved.");
    assert_course(str_contains($section->summary, htmlspecialchars($moduleDefinition['introduction'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')), "Module {$moduleIndex} introduction was not preserved.");
    foreach ($moduleDefinition['activities'] as $activity) $expectedActivities[] = $activity;
}
$pages = array_values($DB->get_records('page', ['course' => $course->id], 'id'));
assert_course(count($pages) === count($expectedActivities), 'Source Activity count was not preserved.');
foreach ($expectedActivities as $index => $activity) {
    $page = $pages[$index];
    $content = $page->content;
    assert_course($page->name === $activity['name'], "Source Activity {$index} name was not preserved.");
    assert_course(str_contains($content, htmlspecialchars($activity['source']['title'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')), "Source Activity {$index} Source title was not preserved.");
    assert_course(str_contains($content, htmlspecialchars($activity['purpose'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')), "Source Activity {$index} purpose was not preserved.");
    assert_course(str_contains($content, htmlspecialchars($activity['instructions'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')), "Source Activity {$index} instructions were not preserved.");
    assert_course(str_contains($content, 'Estimated Activity Duration'), "Source Activity {$index} does not show its estimated duration.");
    assert_course(str_contains($content, $activity['duration_minutes'] . ' minutes'), "Source Activity {$index} activity duration was not preserved.");
    assert_course(str_contains($content, htmlspecialchars($activity['source']['publisher'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')), "Source Activity {$index} publisher was not preserved.");
    assert_course(str_contains($content, ucfirst($activity['source']['source_type'])), "Source Activity {$index} Source type was not preserved.");
    if ($activity['duration_minutes'] === $activity['source']['duration_minutes']) {
        assert_course(!str_contains($content, 'Estimated Source Duration'), "Source Activity {$index} duplicates an equal Source duration.");
    } else {
        assert_course(str_contains($content, 'Estimated Source Duration'), "Source Activity {$index} does not distinguish its Source duration.");
        assert_course(str_contains($content, $activity['source']['duration_minutes'] . ' minutes'), "Source Activity {$index} Source duration was not preserved.");
    }
    assert_course(str_contains($content, 'Instructions'), "Source Activity {$index} does not label its instructions.");
    assert_course(str_contains($content, 'Completion'), "Source Activity {$index} does not explain completion.");
    foreach (['Finish the Source', 'produce the result required by the instructions', 'return to this Course', 'Mark as done'] as $completionText) {
        assert_course(str_contains($content, $completionText), "Source Activity {$index} has incomplete completion guidance.");
    }
    $escapedSourceUrl = htmlspecialchars($activity['source']['url'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    assert_course(substr_count($content, $escapedSourceUrl) === 1, "Source Activity {$index} must contain exactly one Source link.");
    assert_course(str_contains($content, 'target="_blank"'), "Source Activity {$index} Source CTA must open a new tab.");
    assert_course(str_contains($content, 'rel="noopener noreferrer"'), "Source Activity {$index} Source CTA is missing safe external-link attributes.");
    $contentWithoutSourceUrl = str_replace($escapedSourceUrl, '', $content);
    assert_course(!str_contains($contentWithoutSourceUrl, $activity['source']['provider_item_id']), "Source Activity {$index} exposes its provider item ID.");
    assert_course(!str_contains($content, $activity['source']['availability']['checked_at']), "Source Activity {$index} exposes its availability check time.");
    assert_course(!str_contains($content, $activity['source']['access']['evidence_url']), "Source Activity {$index} exposes its access evidence URL.");
}
$courseModules = array_values($DB->get_records('course_modules', ['course' => $course->id], 'id'));
assert_course(count($courseModules) === count($expectedActivities), 'Course contains unexpected components.');
foreach ($courseModules as $courseModule) {
    assert_course($DB->get_field('modules', 'name', ['id' => $courseModule->module]) === 'page', 'Course Package must use only standard Moodle Page Source Activities.');
    $cm = get_coursemodule_from_id('page', $courseModule->id, $course->id, false, MUST_EXIST);
    assert_course($cm->completion == COMPLETION_TRACKING_MANUAL && $cm->completionview == 0, 'Each Source Activity must require explicit learner completion confirmation.');
}
assert_course($DB->count_records('user_enrolments') === 0, 'Course Package unexpectedly contains enrolments.');
assert_course($DB->count_records_select('user', 'id > 2') === 0, 'Course Package unexpectedly contains users.');
assert_course($DB->count_records('grade_grades') === 0, 'Course Package unexpectedly contains grades.');
assert_course($DB->count_records('course_modules_completion') === 0, 'Course Package unexpectedly contains activity completion records.');
assert_course($DB->count_records('course_completions') === 0, 'Course Package unexpectedly contains Course completion records.');
echo "Verified restored Course Definition structure and package hygiene.\n";
echo "ACTIVITY_ID={$courseModules[0]->id}\n";
