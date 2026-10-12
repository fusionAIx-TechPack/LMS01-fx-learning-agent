import 'dart:async';
import 'package:flutter/foundation.dart';
import '../models/course_proposal.dart';
import '../models/job_status.dart';
import '../services/api_service.dart';

enum AppViewTab {
  input,
  review,
  progress,
  history,
}

class CourseGeneratorProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();

  AppViewTab _currentTab = AppViewTab.input;
  AppViewTab get currentTab => _currentTab;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String? _errorMessage;
  String? get errorMessage => _errorMessage;

  List<CourseProposal> _proposals = [];
  List<CourseProposal> get proposals => _proposals;

  int _selectedProposalIndex = 0;
  int get selectedProposalIndex => _selectedProposalIndex;

  CourseProposal? get currentProposal =>
      _proposals.isNotEmpty && _selectedProposalIndex < _proposals.length
          ? _proposals[_selectedProposalIndex]
          : null;

  GenerationJob? _activeJob;
  GenerationJob? get activeJob => _activeJob;

  Timer? _pollingTimer;

  List<CourseProposal> _completedCourses = [];
  List<CourseProposal> get completedCourses => _completedCourses;

  void setTab(AppViewTab tab) {
    _currentTab = tab;
    notifyListeners();
  }

  void selectProposal(int index) {
    if (index >= 0 && index < _proposals.length) {
      _selectedProposalIndex = index;
      notifyListeners();
    }
  }

  /// Analyze raw URLs
  Future<void> analyzeUrls(List<String> rawUrls) async {
    final cleanUrls = rawUrls.map((u) => u.trim()).where((u) => u.isNotEmpty).toList();
    if (cleanUrls.isEmpty) {
      _errorMessage = 'Please enter at least one valid HTTP(S) URL.';
      notifyListeners();
      return;
    }

    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final results = await _apiService.analyzeUrls(cleanUrls);
      _proposals = results;
      _selectedProposalIndex = 0;
      _currentTab = AppViewTab.review;
    } catch (e) {
      _errorMessage = 'Failed to analyze URLs: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Handle spreadsheet upload
  Future<void> uploadSpreadsheet(List<int> bytes, String fileName) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final results = await _apiService.uploadSpreadsheet(bytes, fileName);
      _proposals = results;
      _selectedProposalIndex = 0;
      _currentTab = AppViewTab.review;
    } catch (e) {
      _errorMessage = 'Failed to process spreadsheet: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Update editable fields in proposal during the human review gate
  void updateCurrentProposal({
    String? courseName,
    String? overview,
    int? durationMinutes,
    String? level,
    String? audience,
  }) {
    if (currentProposal == null) return;

    if (courseName != null) currentProposal!.courseName = courseName;
    if (overview != null) currentProposal!.courseOverview = overview;
    if (durationMinutes != null) currentProposal!.courseDurationMinutes = durationMinutes;
    if (level != null) currentProposal!.level = level;
    if (audience != null) currentProposal!.audience = audience;

    notifyListeners();
  }

  /// Approve current proposal and trigger Moodle course creation
  Future<void> approveAndBuildCurrentCourse() async {
    if (currentProposal == null) return;

    currentProposal!.isApproved = true;
    currentProposal!.status = 'packaging';
    _isLoading = true;
    notifyListeners();

    try {
      final job = await _apiService.startBuild(currentProposal!);
      _activeJob = job;
      _currentTab = AppViewTab.progress;

      // Start simulating or polling progress
      _startProgressTracking();
    } catch (e) {
      _errorMessage = 'Build startup failed: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Start progress polling or simulated steps
  void _startProgressTracking() {
    _pollingTimer?.cancel();

    // If connected to real backend, polls every 2 seconds
    int stepCount = 0;
    _pollingTimer = Timer.periodic(const Duration(seconds: 2), (timer) async {
      stepCount++;

      // In mock/offline mode, step through the 5 phases automatically:
      if (_activeJob != null) {
        BuildStep nextStep = _activeJob!.currentStep;
        List<String> newLogs = List.from(_activeJob!.logs);

        if (stepCount == 1) {
          nextStep = BuildStep.synthesizingAi;
          newLogs.add('AI synthesizing modules and finding reference videos...');
        } else if (stepCount == 2) {
          nextStep = BuildStep.compilingDefinition;
          newLogs.add('Validating JSON course brief and compiling definition...');
        } else if (stepCount == 3) {
          nextStep = BuildStep.instantiatingMoodle;
          newLogs.add('Docker container initialized with seed database...');
        } else if (stepCount == 4) {
          nextStep = BuildStep.packagingMbz;
          newLogs.add('Executing moodle-cli/generate.php and creating 5 activities...');
          newLogs.add('Running moodle-cli/backup.php into .mbz package...');
        } else if (stepCount >= 5) {
          nextStep = BuildStep.completed;
          newLogs.add('Clean restoration verified: All 5 activities intact.');
          newLogs.add('Ready for download!');
          timer.cancel();

          // Mark proposal completed
          if (currentProposal != null) {
            currentProposal!.status = 'completed';
            currentProposal!.packagePath = 'output/${_activeJob!.courseSlug}/course-package.mbz';
            if (!_completedCourses.contains(currentProposal!)) {
              _completedCourses.add(currentProposal!);
            }
          }
        }

        _activeJob = GenerationJob(
          jobId: _activeJob!.jobId,
          courseSlug: _activeJob!.courseSlug,
          courseName: _activeJob!.courseName,
          currentStep: nextStep,
          progress: nextStep.progressFraction,
          logs: newLogs,
          mbzDownloadUrl: nextStep == BuildStep.completed
              ? 'http://localhost:8000/api/download/${_activeJob!.courseSlug}.mbz'
              : null,
          createdAt: _activeJob!.createdAt,
        );
        notifyListeners();
      }
    });
  }

  void reset() {
    _pollingTimer?.cancel();
    _proposals = [];
    _activeJob = null;
    _currentTab = AppViewTab.input;
    _errorMessage = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    super.dispose();
  }
}
