<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir . '/completionlib.php');
require_once($CFG->libdir . '/resourcelib.php');
require_once(__DIR__ . '/course_definition.php');

function assert_course(bool $condition, string $message): void {
    if (!$condition) throw new RuntimeException($message);
}

$definition = load_course_definition($argv[1] ?? '');
$course = $DB->get_record('course', ['shortname' => $definition['identity']['shortname']], '*', MUST_EXIST);
$mode = $argv[2] ?? 'structure';

$modulesById = array_values($DB->get_records('course_modules', ['course' => $course->id], 'id'));

if ($mode === 'completion-incomplete' || $mode === 'completion-complete') {
    $userid = filter_var($argv[3] ?? null, FILTER_VALIDATE_INT);
    assert_course($userid !== false && $userid > 0, 'Completion verification requires a valid learner user ID.');
    $overviewModule = $modulesById[0] ?? null;
    assert_course($overviewModule !== null, 'Course has no learner-visible Learning Activity.');
    $completion = new completion_info($course);
    $cm = get_coursemodule_from_id('page', $overviewModule->id, $course->id, false, MUST_EXIST);
    $state = $completion->get_data($cm, false, $userid);
    if ($mode === 'completion-incomplete') {
        assert_course($state->completionstate == COMPLETION_INCOMPLETE, 'The Learning Activity was completed without learner confirmation.');
        echo "Verified that opening an activity does not complete it without learner confirmation.\n";
    } else {
        assert_course($state->completionstate == COMPLETION_COMPLETE, 'The learner confirmation did not complete the Learning Activity.');
        echo "Verified explicit learner completion confirmation.\n";
    }
    exit(0);
}

$structure = $definition['structure'];
$acts = $structure['activities'];

assert_course($course->fullname === $definition['identity']['fullname'], 'Course identity was not preserved.');
assert_course($course->visible == 1, 'Restored Course must be visible.');
assert_course($course->format === 'topics', 'Restored Course must use topic format.');
assert_course($course->enablecompletion == 1, 'Course completion tracking must be enabled.');

$sections = array_values($DB->get_records('course_sections', ['course' => $course->id], 'section'));
assert_course(count($sections) === 1, 'Restored Course must have exactly one section.');
assert_course($sections[0]->name === $structure['section_name'], 'The single section must be named for the Course topic.');

assert_course(count($modulesById) === 5, 'Restored Course must contain exactly five activities.');
$modName = static function ($cm) use ($DB) {
    return $DB->get_field('modules', 'name', ['id' => $cm->module]);
};
$expectedModules = ['page', 'url', 'page', 'assign', 'forum'];
foreach ($expectedModules as $index => $expected) {
    assert_course($modName($modulesById[$index]) === $expected, "Activity {$index} must be a Moodle {$expected} activity.");
}
[$overviewCm, $resourcesCm, $videosCm, $assignmentCm, $discussionCm] = $modulesById;

// --- Course overview page --------------------------------------------------
$overviewPage = $DB->get_record('page', ['id' => get_coursemodule_from_id('page', $overviewCm->id, $course->id, false, MUST_EXIST)->instance], '*', MUST_EXIST);
assert_course($overviewPage->name === $acts['overview']['name'], 'Course overview activity name was not preserved.');
foreach (['Number of Modules', (string) $acts['overview']['module_count'], 'Estimated Time', $acts['overview']['estimated_time_label'], 'Instruction'] as $needle) {
    assert_course(str_contains($overviewPage->content, htmlspecialchars($needle, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')) || str_contains($overviewPage->content, $needle), "Course overview is missing: {$needle}");
}

// --- Main link (URL) ----------------------------------------------------
$urlInstance = $DB->get_record('url', ['id' => get_coursemodule_from_id('url', $resourcesCm->id, $course->id, false, MUST_EXIST)->instance], '*', MUST_EXIST);
assert_course($urlInstance->name === $acts['resources']['name'], 'Main link activity name was not preserved.');
assert_course($urlInstance->externalurl === $acts['resources']['primary_url'], 'Main link URL was not preserved.');
assert_course((int) $urlInstance->display === RESOURCELIB_DISPLAY_NEW, 'The main link must open in a new window.');
assert_course(trim(strip_tags((string) $urlInstance->intro)) === '', 'The main link must have no description.');

// --- Reference videos page ----------------------------------------------
$videosPage = $DB->get_record('page', ['id' => get_coursemodule_from_id('page', $videosCm->id, $course->id, false, MUST_EXIST)->instance], '*', MUST_EXIST);
assert_course($videosPage->name === $acts['videos']['name'], 'Reference videos activity name was not preserved.');
if (count($acts['videos']['items']) > 0) {
    foreach ($acts['videos']['items'] as $index => $item) {
        assert_course(str_contains($videosPage->content, htmlspecialchars($item['title'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')), "Reference videos page is missing video {$index}.");
    }
} else {
    assert_course(str_contains($videosPage->content, 'No additional reference videos'), 'Reference videos page is missing its empty-state text.');
}

// --- Certification assignment ------------------------------------------
$assignCmInfo = get_coursemodule_from_id('assign', $assignmentCm->id, $course->id, false, MUST_EXIST);
$assignInstance = $DB->get_record('assign', ['id' => $assignCmInfo->instance], '*', MUST_EXIST);
assert_course($assignInstance->name === $acts['assignment']['name'], 'Certification assignment name was not preserved.');
assert_course($assignInstance->completionsubmit == 1, 'The certification assignment must complete on submission.');
assert_course($assignCmInfo->completion == COMPLETION_TRACKING_AUTOMATIC, 'The certification assignment must use automatic completion on submit.');
assert_course((int) $assignInstance->grade === 0, 'The certification assignment must not be graded.');
$fileEnabled = $DB->get_field('assign_plugin_config', 'value', ['assignment' => $assignInstance->id, 'plugin' => 'file', 'subtype' => 'assignsubmission', 'name' => 'enabled']);
$textEnabled = $DB->get_field('assign_plugin_config', 'value', ['assignment' => $assignInstance->id, 'plugin' => 'onlinetext', 'subtype' => 'assignsubmission', 'name' => 'enabled']);
assert_course($fileEnabled == 1, 'The certification assignment must accept file submissions.');
assert_course($textEnabled == 0, 'The certification assignment must not accept online-text submissions.');

// --- Discussion forum ------------------------------------------------
$forumCmInfo = get_coursemodule_from_id('forum', $discussionCm->id, $course->id, false, MUST_EXIST);
$forumInstance = $DB->get_record('forum', ['id' => $forumCmInfo->instance], '*', MUST_EXIST);
assert_course($forumInstance->name === $acts['discussion']['name'], 'Discussion forum name was not preserved.');
assert_course($forumInstance->type === 'general', 'Discussion forum must be a general discussion forum.');
assert_course((int) $forumInstance->assessed === 0 && (int) $forumInstance->grade_forum === 0, 'The discussion forum must not be graded.');

// --- Completion model ---------------------------------------------------
foreach ([$overviewCm, $resourcesCm, $videosCm, $discussionCm] as $index => $cmRow) {
    $cm = get_coursemodule_from_id(false, $cmRow->id, $course->id, false, MUST_EXIST);
    assert_course($cm->completion == COMPLETION_TRACKING_MANUAL && $cm->completionview == 0, "Activity {$index} must require explicit learner completion confirmation.");
}

// --- Package hygiene --------------------------------------------------
assert_course($DB->count_records('user_enrolments') === 0, 'Course Package unexpectedly contains enrolments.');
assert_course($DB->count_records_select('user', 'id > 2') === 0, 'Course Package unexpectedly contains users.');
assert_course($DB->count_records('grade_grades') === 0, 'Course Package unexpectedly contains grades.');
assert_course($DB->count_records('course_modules_completion') === 0, 'Course Package unexpectedly contains activity completion records.');
assert_course($DB->count_records('course_completions') === 0, 'Course Package unexpectedly contains Course completion records.');
assert_course($DB->count_records('assign_submission') === 0, 'Course Package unexpectedly contains assignment submissions.');
assert_course($DB->count_records('forum_discussions') === 0 && $DB->count_records('forum_posts') === 0, 'Course Package unexpectedly contains forum posts.');

// --- No provenance leakage into learner-visible content -------------
$learnerVisible = implode("\n", [
    $overviewPage->intro, $overviewPage->content,
    $urlInstance->intro,
    $videosPage->intro, $videosPage->content,
    $assignInstance->intro,
    $forumInstance->intro,
    $sections[0]->summary,
]);
// A Source URL may legitimately contain its own provider_item_id as a path
// segment; strip the (escaped) Source and video links before checking that no
// internal identifier or evidence link is exposed as visible text.
$withoutLinks = str_replace(
    htmlspecialchars($definition['brief']['source_url'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'),
    '',
    $learnerVisible
);
foreach (array_merge($definition['brief']['sources'], $definition['brief']['reference_videos']) as $linked) {
    $withoutLinks = str_replace(htmlspecialchars($linked['url'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'), '', $withoutLinks);
}
foreach ($definition['brief']['sources'] as $index => $source) {
    assert_course(!str_contains($withoutLinks, $source['provider_item_id']), "Source {$index} provider item ID leaked into learner-visible content.");
    assert_course(!str_contains($learnerVisible, $source['access']['evidence_url']), "Source {$index} access evidence URL leaked into learner-visible content.");
    assert_course(!str_contains($learnerVisible, $source['availability']['checked_at']), "Source {$index} availability check time leaked into learner-visible content.");
}

echo "Verified restored Course Definition structure and package hygiene.\n";
echo "OVERVIEW_ID={$overviewCm->id}\n";
echo "RESOURCES_ID={$resourcesCm->id}\n";
echo "VIDEOS_ID={$videosCm->id}\n";
echo "ASSIGNMENT_ID={$assignmentCm->id}\n";
echo "DISCUSSION_ID={$discussionCm->id}\n";
echo "ACTIVITY_ID={$overviewCm->id}\n";
