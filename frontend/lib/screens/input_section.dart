import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:file_picker/file_picker.dart';
import '../providers/course_generator_provider.dart';

class InputSection extends StatefulWidget {
  const InputSection({super.key});

  @override
  State<InputSection> createState() => _InputSectionState();
}

class _InputSectionState extends State<InputSection>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final TextEditingController _singleUrlController = TextEditingController();
  final TextEditingController _multiUrlController = TextEditingController();
  String? _pickedFileName;
  Uint8List? _pickedFileBytes;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _singleUrlController.dispose();
    _multiUrlController.dispose();
    super.dispose();
  }

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['xlsx', 'csv'],
      withData: true,
    );

    if (result != null && result.files.isNotEmpty) {
      final file = result.files.first;
      setState(() {
        _pickedFileName = file.name;
        _pickedFileBytes = file.bytes;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<CourseGeneratorProvider>();
    final theme = Theme.of(context);

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 860),
        child: Card(
          elevation: 6,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: BorderSide(color: Colors.white.withOpacity(0.08)),
          ),
          color: const Color(0xFF131B2E),
          child: Padding(
            padding: const EdgeInsets.all(32.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.blue.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.auto_stories,
                        color: Colors.blueAccent,
                        size: 32,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Create Moodle Learning Course',
                            style: theme.textTheme.titleLarge?.copyWith(
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Provide a public course URL, paste a list, or upload a spreadsheet. The AI structures it into standard Moodle .mbz packages.',
                            style: TextStyle(color: Colors.grey.shade400, fontSize: 13),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 28),

                // Tab Selector
                Container(
                  decoration: BoxDecoration(
                    color: const Color(0xFF1E293B),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: TabBar(
                    controller: _tabController,
                    indicatorSize: TabBarIndicatorSize.tab,
                    indicator: BoxDecoration(
                      color: Colors.blueAccent,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    labelColor: Colors.white,
                    unselectedLabelColor: Colors.grey.shade400,
                    tabs: const [
                      Tab(icon: Icon(Icons.link, size: 20), text: 'Single URL'),
                      Tab(icon: Icon(Icons.format_list_bulleted, size: 20), text: 'Multiple URLs'),
                      Tab(icon: Icon(Icons.table_chart, size: 20), text: 'Upload Spreadsheet'),
                    ],
                  ),
                ),
                const SizedBox(height: 24),

                // Tab Content
                SizedBox(
                  height: 220,
                  child: TabBarView(
                    controller: _tabController,
                    children: [
                      // Single URL
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Enter Source URL',
                            style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70),
                          ),
                          const SizedBox(height: 8),
                          TextField(
                            controller: _singleUrlController,
                            style: const TextStyle(color: Colors.white),
                            decoration: InputDecoration(
                              hintText: 'https://academy.pega.com/topic/generative-ai-pega/v1',
                              hintStyle: TextStyle(color: Colors.grey.shade600),
                              prefixIcon: const Icon(Icons.search, color: Colors.blueAccent),
                              filled: true,
                              fillColor: const Color(0xFF0F172A),
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(10),
                                borderSide: BorderSide(color: Colors.grey.shade800),
                              ),
                            ),
                          ),
                          const SizedBox(height: 12),
                          Text(
                            'Example: Microsoft Learn, Coursera, vendor tutorials, or documentation pages.',
                            style: TextStyle(color: Colors.grey.shade500, fontSize: 12),
                          ),
                        ],
                      ),

                      // Multiple URLs
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Enter Multiple URLs (One per line)',
                            style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70),
                          ),
                          const SizedBox(height: 8),
                          Expanded(
                            child: TextField(
                              controller: _multiUrlController,
                              maxLines: 5,
                              style: const TextStyle(color: Colors.white),
                              decoration: InputDecoration(
                                hintText: "https://learn.microsoft.com/en-us/training/paths/ai-concepts-developers/\nhttps://academy.pega.com/topic/generative-ai-pega/v1",
                                hintStyle: TextStyle(color: Colors.grey.shade600),
                                filled: true,
                                fillColor: const Color(0xFF0F172A),
                                border: OutlineInputBorder(
                                  borderRadius: BorderRadius.circular(10),
                                  borderSide: BorderSide(color: Colors.grey.shade800),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),

                      // Spreadsheet Upload
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          InkWell(
                            onTap: _pickFile,
                            borderRadius: BorderRadius.circular(12),
                            child: Container(
                              width: double.infinity,
                              padding: const EdgeInsets.symmetric(vertical: 28),
                              decoration: BoxDecoration(
                                color: const Color(0xFF0F172A),
                                borderRadius: BorderRadius.circular(12),
                                border: Border.all(
                                  color: Colors.blueAccent.withOpacity(0.4),
                                  style: BorderStyle.solid,
                                  width: 1.5,
                                ),
                              ),
                              child: Column(
                                children: [
                                  Icon(
                                    _pickedFileName != null ? Icons.check_circle : Icons.cloud_upload_outlined,
                                    size: 40,
                                    color: _pickedFileName != null ? Colors.greenAccent : Colors.blueAccent,
                                  ),
                                  const SizedBox(height: 10),
                                  Text(
                                    _pickedFileName ?? 'Click to upload Excel (.xlsx) or CSV (.csv)',
                                    style: TextStyle(
                                      color: _pickedFileName != null ? Colors.white : Colors.grey.shade300,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    'Spreadsheet only needs a column with course URLs',
                                    style: TextStyle(color: Colors.grey.shade500, fontSize: 12),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                if (provider.errorMessage != null) ...[
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.red.withOpacity(0.15),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.redAccent.withOpacity(0.5)),
                    ),
                    child: Text(
                      provider.errorMessage!,
                      style: const TextStyle(color: Colors.redAccent, fontSize: 13),
                    ),
                  ),
                ],

                const SizedBox(height: 20),

                // Action Button
                SizedBox(
                  height: 52,
                  child: ElevatedButton(
                    onPressed: provider.isLoading
                        ? null
                        : () {
                            if (_tabController.index == 0) {
                              provider.analyzeUrls([_singleUrlController.text]);
                            } else if (_tabController.index == 1) {
                              final urls = _multiUrlController.text.split('\n');
                              provider.analyzeUrls(urls);
                            } else {
                              if (_pickedFileBytes != null && _pickedFileName != null) {
                                provider.uploadSpreadsheet(_pickedFileBytes!, _pickedFileName!);
                              } else {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('Please select an Excel or CSV file first')),
                                );
                              }
                            }
                          },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blueAccent,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      elevation: 4,
                    ),
                    child: provider.isLoading
                        ? const Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                              ),
                              SizedBox(width: 12),
                              Text('Analyzing Content & Extracting Structure...', style: TextStyle(color: Colors.white)),
                            ],
                          )
                        : const Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.bolt, color: Colors.white),
                              SizedBox(width: 8),
                              Text(
                                'Analyze & Propose Course',
                                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                              ),
                            ],
                          ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
