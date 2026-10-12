import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/job_status.dart';
import '../providers/course_generator_provider.dart';

class ProgressScreen extends StatelessWidget {
  const ProgressScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<CourseGeneratorProvider>();
    final job = provider.activeJob;

    if (job == null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('No active build job.', style: TextStyle(color: Colors.white)),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: () => provider.setTab(AppViewTab.input),
              child: const Text('Go to Input'),
            ),
          ],
        ),
      );
    }

    final isDone = job.currentStep == BuildStep.completed;

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 900),
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(vertical: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Main Progress Card
              Card(
                elevation: 6,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(color: Colors.white.withOpacity(0.08)),
                ),
                color: const Color(0xFF131B2E),
                child: Padding(
                  padding: const EdgeInsets.all(32.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Header
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: isDone
                                  ? Colors.green.withOpacity(0.15)
                                  : Colors.blueAccent.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Icon(
                              isDone ? Icons.check_circle : Icons.precision_manufacturing,
                              color: isDone ? Colors.greenAccent : Colors.blueAccent,
                              size: 32,
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  isDone ? 'Packaging Completed!' : 'Building Moodle Course Package',
                                  style: const TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  job.courseName,
                                  style: TextStyle(color: Colors.grey.shade400, fontSize: 13),
                                ),
                              ],
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                            decoration: BoxDecoration(
                              color: isDone
                                  ? Colors.green.withOpacity(0.2)
                                  : Colors.blue.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(
                              isDone ? 'READY' : '${(job.progress * 100).toInt()}%',
                              style: TextStyle(
                                color: isDone ? Colors.greenAccent : Colors.blueAccent,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 24),

                      // Progress Bar
                      ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: LinearProgressIndicator(
                          value: job.progress,
                          minHeight: 10,
                          backgroundColor: const Color(0xFF1E293B),
                          valueColor: AlwaysStoppedAnimation<Color>(
                            isDone ? Colors.greenAccent : Colors.blueAccent,
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),

                      // Current Step Status
                      Text(
                        job.currentStep.label,
                        style: TextStyle(
                          color: isDone ? Colors.greenAccent : Colors.lightBlueAccent,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      const SizedBox(height: 28),

                      // 5 Step Horizontal Indicator
                      _buildStepStages(job.currentStep),
                      const SizedBox(height: 28),

                      // Real-time Console Log Box
                      const Text(
                        'Process Logs',
                        style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white70),
                      ),
                      const SizedBox(height: 8),
                      Container(
                        height: 160,
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: const Color(0xFF090D16),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: Colors.white.withOpacity(0.06)),
                        ),
                        child: ListView.builder(
                          itemCount: job.logs.length,
                          itemBuilder: (context, index) {
                            return Padding(
                              padding: const EdgeInsets.symmetric(vertical: 2.0),
                              child: Text(
                                '> ${job.logs[index]}',
                                style: const TextStyle(
                                  fontFamily: 'monospace',
                                  fontSize: 12,
                                  color: Color(0xFF38BDF8),
                                ),
                              ),
                            );
                          },
                        ),
                      ),

                      if (isDone) ...[
                        const SizedBox(height: 28),
                        Container(
                          padding: const EdgeInsets.all(20),
                          decoration: BoxDecoration(
                            color: Colors.green.withOpacity(0.12),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: Colors.greenAccent.withOpacity(0.4)),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              Row(
                                children: [
                                  const Icon(Icons.download_done, color: Colors.greenAccent, size: 28),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        const Text(
                                          'Course Package Ready (.mbz)',
                                          style: TextStyle(
                                            color: Colors.greenAccent,
                                            fontWeight: FontWeight.bold,
                                            fontSize: 16,
                                          ),
                                        ),
                                        Text(
                                          'Validated with all 5 activities (Overview, Topic URL, Videos, Certification, Forum).',
                                          style: TextStyle(color: Colors.grey.shade300, fontSize: 13),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 16),
                              ElevatedButton.icon(
                                onPressed: () {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                      content: Text('Downloading course-package.mbz for ${job.courseSlug}...'),
                                      backgroundColor: Colors.green,
                                    ),
                                  );
                                },
                                icon: const Icon(Icons.download, color: Colors.black87),
                                label: const Text(
                                  'Download .mbz Package',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 15,
                                    color: Colors.black87,
                                  ),
                                ),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.greenAccent,
                                  padding: const EdgeInsets.symmetric(vertical: 16),
                                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],

                      const SizedBox(height: 24),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          TextButton.icon(
                            onPressed: () => provider.reset(),
                            icon: const Icon(Icons.add, color: Colors.blueAccent),
                            label: const Text('Create Another Course', style: TextStyle(color: Colors.blueAccent)),
                          ),
                          const SizedBox(width: 12),
                          ElevatedButton.icon(
                            onPressed: () => provider.setTab(AppViewTab.history),
                            icon: const Icon(Icons.library_books),
                            label: const Text('View All Courses'),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStepStages(BuildStep current) {
    final stages = [
      {'title': 'Scrape URL', 'step': BuildStep.scrapingUrl},
      {'title': 'AI Synthesis', 'step': BuildStep.synthesizingAi},
      {'title': 'Definition', 'step': BuildStep.compilingDefinition},
      {'title': 'Moodle Setup', 'step': BuildStep.instantiatingMoodle},
      {'title': 'Package .mbz', 'step': BuildStep.packagingMbz},
    ];

    return Row(
      children: List.generate(stages.length, (index) {
        final stage = stages[index];
        final stepEnum = stage['step'] as BuildStep;
        final isPassed = current.index > stepEnum.index || current == BuildStep.completed;
        final isActive = current == stepEnum;

        return Expanded(
          child: Column(
            children: [
              Container(
                width: 32,
                height: 32,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: isPassed
                      ? Colors.greenAccent
                      : (isActive ? Colors.blueAccent : const Color(0xFF1E293B)),
                ),
                child: Center(
                  child: isPassed
                      ? const Icon(Icons.check, size: 18, color: Colors.black87)
                      : Text(
                          '${index + 1}',
                          style: TextStyle(
                            color: isActive ? Colors.white : Colors.grey.shade500,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                ),
              ),
              const SizedBox(height: 6),
              Text(
                stage['title'] as String,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 11,
                  color: isPassed || isActive ? Colors.white : Colors.grey.shade600,
                  fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ],
          ),
        );
      }),
    );
  }
}
