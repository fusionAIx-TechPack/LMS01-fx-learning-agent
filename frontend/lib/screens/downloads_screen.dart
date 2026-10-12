import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/course_proposal.dart';
import '../providers/course_generator_provider.dart';

class DownloadsScreen extends StatelessWidget {
  const DownloadsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<CourseGeneratorProvider>();
    final completed = provider.completedCourses;

    // Also include pre-existing sample courses from output folder
    final List<Map<String, dynamic>> defaultCourses = [
      {
        'name': 'AI Concepts for Developers and Technology Professionals',
        'slug': 'ai-concepts-for-developers',
        'duration': '231 mins',
        'level': 'beginner',
        'status': 'Ready',
      },
      {
        'name': 'Generative AI with Pega Constellation',
        'slug': 'pega-genai',
        'duration': '120 mins',
        'level': 'intermediate',
        'status': 'Ready',
      },
      {
        'name': 'Custom Open-Weight LLM for Financial Crime Compliance',
        'slug': 'custom-open-weight-llm-financial-crime-compliance',
        'duration': '180 mins',
        'level': 'advanced',
        'status': 'Ready',
      },
      {
        'name': 'Build an Agent with Microsoft Copilot Studio',
        'slug': 'build-an-agent-copilot-studio',
        'duration': '90 mins',
        'level': 'beginner',
        'status': 'Ready',
      },
    ];

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 1000),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Course Library & Moodle Packages',
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'All generated courses stored in output/. Download .mbz to import into Moodle.',
                        style: TextStyle(color: Colors.grey.shade400, fontSize: 13),
                      ),
                    ],
                  ),
                  ElevatedButton.icon(
                    onPressed: () => provider.setTab(AppViewTab.input),
                    icon: const Icon(Icons.add, color: Colors.white),
                    label: const Text('Generate New Course', style: TextStyle(color: Colors.white)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blueAccent,
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Courses Card
              Card(
                elevation: 6,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(color: Colors.white.withOpacity(0.08)),
                ),
                color: const Color(0xFF131B2E),
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      // Table header
                      Container(
                        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                        decoration: BoxDecoration(
                          color: const Color(0xFF1E293B),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Row(
                          children: [
                            Expanded(flex: 4, child: Text('Course Name', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white70))),
                            Expanded(flex: 2, child: Text('Duration', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white70))),
                            Expanded(flex: 2, child: Text('Level', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white70))),
                            Expanded(flex: 2, child: Text('Status', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white70))),
                            Expanded(flex: 2, child: Text('Action', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white70))),
                          ],
                        ),
                      ),
                      const SizedBox(height: 8),

                      // Newly generated courses first
                      ...completed.map((course) {
                        return _buildRow(
                          context,
                          title: course.courseName,
                          duration: '${course.courseDurationMinutes} mins',
                          level: course.level,
                          status: 'Just Built',
                          isNew: true,
                        );
                      }),

                      // Default historical courses
                      ...defaultCourses.map((c) {
                        return _buildRow(
                          context,
                          title: c['name'] as String,
                          duration: c['duration'] as String,
                          level: c['level'] as String,
                          status: c['status'] as String,
                          isNew: false,
                        );
                      }),
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

  Widget _buildRow(
    BuildContext context, {
    required String title,
    required String duration,
    required String level,
    required String status,
    required bool isNew,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
      decoration: BoxDecoration(
        border: Border(bottom: BorderSide(color: Colors.white.withOpacity(0.04))),
      ),
      child: Row(
        children: [
          Expanded(
            flex: 4,
            child: Row(
              children: [
                Icon(
                  Icons.school,
                  size: 20,
                  color: isNew ? Colors.greenAccent : Colors.blueAccent,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    title,
                    style: const TextStyle(fontWeight: FontWeight.w600, color: Colors.white),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            flex: 2,
            child: Text(duration, style: TextStyle(color: Colors.grey.shade400)),
          ),
          Expanded(
            flex: 2,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.blueGrey.withOpacity(0.2),
                borderRadius: BorderRadius.circular(6),
              ),
              child: Text(
                level.toUpperCase(),
                style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white70),
              ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Row(
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: isNew ? Colors.greenAccent : Colors.lightBlueAccent,
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  status,
                  style: TextStyle(
                    color: isNew ? Colors.greenAccent : Colors.lightBlueAccent,
                    fontSize: 13,
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            flex: 2,
            child: Align(
              alignment: Alignment.centerRight,
              child: ElevatedButton.icon(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Downloading .mbz package for: $title')),
                  );
                },
                icon: const Icon(Icons.download, size: 16, color: Colors.white),
                label: const Text('.mbz', style: TextStyle(fontSize: 12, color: Colors.white)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF2563EB),
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
