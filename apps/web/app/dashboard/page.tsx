
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, BarChart2, Loader2, Rocket } from 'lucide-react';
import NewProjectModal from '@/components/new-project-modal';
// import { createClientComponentClient } from '@supabase/ssr';

const DashboardPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [chartHtml, setChartHtml] = useState<string | null>(null);
  const [xColumn, setXColumn] = useState('');
  const [yColumn, setYColumn] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isCreatingProject, setIsCreatingProject] = useState(false);

  // const supabase = createClientComponentClient();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setMessage('');
      setAnalysisResults(null);
      setChartHtml(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first.');
      return;
    }

    setUploading(true);
    setMessage('');
    setAnalysisResults(null);
    setChartHtml(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`http://localhost:8000/api/data-analysis/analyze-csv`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`File uploaded and analyzed successfully.`);
        setAnalysisResults(data);

        // Attempt to generate chart if columns are selected
        if (xColumn && yColumn) {
          const chartFormData = new FormData();
          chartFormData.append('file', selectedFile);
          chartFormData.append('x_column', xColumn);
          chartFormData.append('y_column', yColumn);

          const chartResponse = await fetch(`http://localhost:8000/api/data-analysis/generate-chart`, {
            method: 'POST',
            body: chartFormData,
          });

          const chartData = await chartResponse.json();

          if (chartResponse.ok) {
            setChartHtml(chartData.chart_html);
          } else {
            setMessage(chartData.detail || 'Chart generation failed.');
          }
        }

      } else {
        setMessage(data.detail || 'File analysis failed.');
      }
    } catch (error) {
      setMessage('An unexpected error occurred during file analysis.');
    }

    setUploading(false);
  };

  const handleCreateProject = async (projectName: string) => {
    setIsCreatingProject(true);
    setMessage('');

    try {
      // const { data: { session } } = await supabase.auth.getSession();
      const session = { access_token: "" }; // Placeholder
      if (!session) {
        setMessage('User not authenticated. Please log in to create a project.');
        setIsCreatingProject(false);
        return;
      }

      const response = await fetch(`http://localhost:8000/api/projects/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({ name: projectName, description: "" }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`Project '${data.name}' created successfully!`);
        setIsModalOpen(false);
        // Optionally redirect to the new project's page or collaboratory
      } else {
        setMessage(data.detail || 'Failed to create project.');
      }
    } catch (error) {
      setMessage('An unexpected error occurred during project creation.');
    }

    setIsCreatingProject(false);
  };

  return (
    <div className="min-h-screen bg-[#141313] flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-2xl p-8 space-y-6 bg-[#1F1F1F] rounded-2xl shadow-lg text-white"
      >
        <h1 className="text-3xl font-bold text-center">Dashboard</h1>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">Start a New Project</h2>
          <motion.button
            onClick={() => setIsModalOpen(true)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full py-3 font-semibold text-white bg-[#615EFF] rounded-lg hover:bg-[#4E4AFF] transition-colors duration-300 flex items-center justify-center"
          >
            <Rocket className="mr-2 h-4 w-4" />
            New Project
          </motion.button>
        </div>

        <div className="space-y-4 mt-8">
          <h2 className="text-2xl font-semibold">Upload Data for Visualization</h2>
          <input
            type="file"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-300
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-[#615EFF] file:text-white
              hover:file:bg-[#4E4AFF]"
          />
          {selectedFile && (
            <p className="text-sm text-gray-400">Selected file: {selectedFile.name}</p>
          )}

          {analysisResults && analysisResults.columns && (
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">Chart Columns (Optional)</h3>
              <div>
                <label htmlFor="x-column" className="block text-sm font-medium text-gray-300">X-Axis Column</label>
                <select
                  id="x-column"
                  value={xColumn}
                  onChange={(e) => setXColumn(e.target.value)}
                  className="mt-1 block w-full px-3 py-2 bg-[#1F1F1F] border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-[#615EFF]"
                >
                  <option value="">Select X-Column</option>
                  {analysisResults.columns.map((col: string) => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="y-column" className="block text-sm font-medium text-gray-300">Y-Axis Column</label>
                <select
                  id="y-column"
                  value={yColumn}
                  onChange={(e) => setYColumn(e.target.value)}
                  className="mt-1 block w-full px-3 py-2 bg-[#1F1F1F] border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-[#615EFF]"
                >
                  <option value="">Select Y-Column</option>
                  {analysisResults.columns.map((col: string) => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
              </div>
            </div>
          )}

          <motion.button
            onClick={handleUpload}
            disabled={uploading || !selectedFile}
            whileHover={{ scale: uploading || !selectedFile ? 1 : 1.05 }}
            whileTap={{ scale: uploading || !selectedFile ? 1 : 0.95 }}
            className="w-full py-3 font-semibold text-white bg-[#0050F0] rounded-lg hover:bg-[#0040D0] transition-colors duration-300 flex items-center justify-center disabled:opacity-50"
          >
            {uploading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Uploading...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Upload File
              </>
            )}
          </motion.button>
          {message && <p className="text-center text-white">{message}</p>}
        </div>

        <div className="space-y-4 mt-8">
          <h2 className="text-2xl font-semibold">Data Visualization Showcase</h2>
          {chartHtml ? (
            <div className="bg-gray-800 p-4 rounded-lg overflow-auto" dangerouslySetInnerHTML={{ __html: chartHtml }} />
          ) : analysisResults ? (
            <div className="bg-gray-800 p-4 rounded-lg overflow-auto">
              <h3 className="text-xl font-semibold mb-2">Analysis Results:</h3>
              <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(analysisResults, null, 2)}</pre>
            </div>
          ) : (
            <div className="w-full h-64 bg-gray-700 rounded-lg flex items-center justify-center text-gray-400">
              <BarChart2 className="h-16 w-16" />
              <p>Visualization will appear here</p>
            </div>
          )}
        </div>
      </motion.div>

      <NewProjectModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSubmit={handleCreateProject}
          isLoading={isCreatingProject}
        />
    </div>
  );
};

export default DashboardPage;
