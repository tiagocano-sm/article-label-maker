"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Upload, Download, FileText, Stethoscope, CheckCircle, BarChart3 } from "lucide-react"
import { ApiService, type ClassifyArticleResponse } from "@/services/api"
import { Dashboard } from "@/components/dashboard"

export default function ArticleLabelMaker() {
  const [csvFile, setCsvFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [csvProcessed, setCsvProcessed] = useState(false)
  const [classificationResult, setClassificationResult] = useState<ClassifyArticleResponse | null>(null)
  const [manualForm, setManualForm] = useState({
    title: "",
    abstract: "",
  })
  const [csvResult, setCsvResult] = useState<{ filename: string; blob: Blob } | null>(null)
  const [activeTab, setActiveTab] = useState("dashboard")

  const handleCsvFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file && file.type === "text/csv") {
      setCsvFile(file)
      setCsvProcessed(false)
      setClassificationResult(null)
      setCsvResult(null)
    }
  }

  const handleCsvUpload = async () => {
    if (csvFile) {
      setIsProcessing(true)
      try {
        const response = await ApiService.classifyArticlesInCSV(csvFile)
        // Download the processed file
        const blob = await ApiService.downloadProcessedCSV(response.output_filename)
        setCsvResult({ filename: response.output_filename, blob })
        setCsvProcessed(true)
      } catch (error) {
        console.error("Error processing CSV:", error)
        console.error("Error details:", error)
        alert(`Error processing CSV: ${error instanceof Error ? error.message : 'Unknown error'}`)
      } finally {
        setIsProcessing(false)
      }
    }
  }

  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (manualForm.title && manualForm.abstract) {
      setIsProcessing(true)
      try {
        const response = await ApiService.classifyArticle({
          title: manualForm.title,
          abstract: manualForm.abstract,
        })
        setClassificationResult(response)
      } catch (error) {
        console.error("Error classifying article:", error)
        alert(`Error classifying article: ${error instanceof Error ? error.message : 'Unknown error'}`)
      } finally {
        setIsProcessing(false)
      }
    }
  }

  const handleDownload = () => {
    if (csvResult) {
      const url = URL.createObjectURL(csvResult.blob)
      const a = document.createElement("a")
      a.href = url
      a.download = csvResult.filename
      a.click()
      URL.revokeObjectURL(url)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-teal-50">
      {/* Header */}
      <header className="border-b border-blue-200 bg-white shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-blue-500 to-teal-500 rounded-xl shadow-lg">
              <Stethoscope className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-800">Article Label Maker</h1>
              <p className="text-blue-600 font-medium">Classify scientific articles with AI-powered labeling</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Input Section */}
          <Card className="shadow-lg border-blue-100">
            <CardHeader className="bg-gradient-to-r from-blue-50 to-teal-50 bg-transparent">
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <FileText className="w-6 h-6 text-blue-600" />
                Article Classification
              </CardTitle>
              <CardDescription className="text-lg text-gray-700 leading-relaxed bg-transparent font-normal">
                Upload a CSV file with multiple articles or manually input a single article for classification
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-3 bg-blue-50">
                  <TabsTrigger value="dashboard" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white">
                    <BarChart3 className="w-4 h-4 mr-2" />
                    Dashboard(test)
                  </TabsTrigger>
                  <TabsTrigger value="csv" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white">
                    CSV Upload
                  </TabsTrigger>
                  <TabsTrigger
                    value="manual"
                    className="data-[state=active]:bg-blue-500 data-[state=active]:text-white"
                  >
                    Manual Input
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="dashboard" className="space-y-6">
                  <Dashboard />
                </TabsContent>

                <TabsContent value="csv" className="space-y-6">
                  {/* CSV Structure Information */}
                  <Card className="border-blue-100 bg-gradient-to-r from-blue-50 to-teal-50">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-gray-800">
                        <FileText className="w-5 h-5 text-blue-600" />
                        CSV File Requirements
                      </CardTitle>
                      <CardDescription className="text-gray-700">
                        Your CSV file must have exactly 2 columns with the following structure:
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="bg-white rounded-lg p-4 border border-blue-200">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="font-semibold text-blue-700 mb-2">Column 1: title</p>
                            <p className="text-gray-600">Article title (required, cannot be empty)</p>
                          </div>
                          <div>
                            <p className="font-semibold text-blue-700 mb-2">Column 2: abstract</p>
                            <p className="text-gray-600">Article abstract (required, cannot be empty)</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="bg-white rounded-lg p-4 border border-blue-200">
                        <p className="font-semibold text-gray-800 mb-2">Example CSV Structure:</p>
                        <div className="bg-gray-50 rounded p-3 font-mono text-sm">
                          <div className="text-blue-600">title,abstract</div>
                          <div className="text-gray-700">"Deep Learning for Computer Vision","This paper presents..."</div>
                          <div className="text-gray-700">"Machine Learning in Healthcare","This study investigates..."</div>
                        </div>
                      </div>
                      
                      <div className="flex justify-center">
                        <Button
                          variant="outline"
                          size="sm"
                          className="border-blue-200 text-blue-700 hover:bg-blue-50"
                          onClick={() => {
                            const csvContent = 'title,abstract\n"Deep Learning for Computer Vision","This paper presents a novel approach to computer vision using deep learning techniques."\n"Machine Learning in Healthcare","This study investigates the use of machine learning algorithms for medical diagnosis."\n"Natural Language Processing","We explore the application of transformer models in NLP tasks."\n"Robotics Systems","We present a comprehensive framework for autonomous robotics."\n"Data Science in Finance","This research examines the application of data science techniques in financial markets."'
                            const blob = new Blob([csvContent], { type: 'text/csv' })
                            const url = URL.createObjectURL(blob)
                            const a = document.createElement('a')
                            a.href = url
                            a.download = 'sample_articles.csv'
                            a.click()
                            URL.revokeObjectURL(url)
                          }}
                        >
                          Download Sample CSV
                        </Button>
                      </div>
                    </CardContent>
                  </Card>

                  {/* File Upload Section */}
                  <div className="border-2 border-dashed border-blue-200 rounded-lg p-8 text-center bg-blue-50/30">
                    <Upload className="w-12 h-12 text-blue-500 mx-auto mb-4" />
                    <div className="space-y-2">
                      <p className="text-lg font-semibold text-gray-800">Upload your CSV file</p>
                      <p className="text-blue-600">Select a CSV file containing article titles and abstracts</p>
                    </div>
                    <div className="mt-4">
                      <label className="inline-block">
                        <input type="file" accept=".csv" onChange={handleCsvFileSelect} className="hidden" />
                        <Button
                          type="button"
                          variant="outline"
                          className="border-blue-200 hover:bg-blue-50 text-blue-700 bg-transparent"
                          onClick={() => document.querySelector('input[type="file"]')?.click()}
                        >
                          Choose File
                        </Button>
                      </label>
                    </div>
                  </div>

                  {csvFile && (
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-teal-50 rounded-lg border border-blue-200">
                        <div className="flex items-center gap-3">
                          <FileText className="w-5 h-5 text-blue-600" />
                          <div>
                            <p className="font-semibold text-gray-800">{csvFile.name}</p>
                            <p className="text-sm text-blue-600">{(csvFile.size / 1024).toFixed(1)} KB</p>
                          </div>
                        </div>
                        {!isProcessing && !csvProcessed && (
                          <Button onClick={handleCsvUpload} className="bg-blue-600 hover:bg-blue-700 text-white">
                            <Upload className="w-4 h-4 mr-2" />
                            Upload
                          </Button>
                        )}
                      </div>

                      {(isProcessing || csvProcessed) && (
                        <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200">
                          <div className="flex items-center gap-3">
                            {isProcessing ? (
                              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>
                            ) : (
                              <CheckCircle className="w-5 h-5 text-green-600" />
                            )}
                            <div>
                              <p className="font-semibold text-gray-800">{csvFile.name}</p>
                              <p className="text-sm text-blue-600">
                                {isProcessing ? "Processing..." : "Ready for download"}
                              </p>
                            </div>
                          </div>
                          {csvProcessed && !isProcessing && (
                            <Button onClick={handleDownload} className="bg-green-600 hover:bg-green-700 text-white">
                              <Download className="w-4 h-4 mr-2" />
                              Download Results
                            </Button>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="manual" className="space-y-4">
                  <form onSubmit={handleManualSubmit} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="title" className="text-gray-800 font-medium">
                        Article Title
                      </Label>
                      <Input
                        id="title"
                        placeholder="Enter the article title..."
                        value={manualForm.title}
                        onChange={(e) => setManualForm((prev) => ({ ...prev, title: e.target.value }))}
                        className="border-blue-200 focus:border-blue-500"
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="abstract" className="text-gray-800 font-medium">
                        Abstract
                      </Label>
                      <Textarea
                        id="abstract"
                        placeholder="Paste the article abstract here..."
                        value={manualForm.abstract}
                        onChange={(e) => setManualForm((prev) => ({ ...prev, abstract: e.target.value }))}
                        rows={6}
                        className="border-blue-200 focus:border-blue-500"
                        required
                      />
                    </div>

                    <Button
                      type="submit"
                      className="w-full bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white font-semibold py-3"
                      disabled={isProcessing || !manualForm.title || !manualForm.abstract}
                    >
                      {isProcessing ? "Classifying..." : "Classify Article"}
                    </Button>
                  </form>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          {/* Results Section - Only show for manual input */}
          {activeTab === "manual" && (isProcessing || classificationResult) && (
            <Card className="shadow-lg border-green-100">
              <CardHeader className="bg-gradient-to-r from-green-50 to-blue-50">
                <CardTitle className="text-gray-800">Classification Results</CardTitle>
                <CardDescription className="text-green-700">
                  AI-generated labels for the submitted article
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                {isProcessing ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                    <span className="ml-3 text-blue-600 font-medium">Processing article...</span>
                  </div>
                ) : classificationResult ? (
                  <div className="space-y-4">
                    <div className="space-y-3">
                      <div>
                        <p className="text-sm text-green-700 font-medium mb-2">Article:</p>
                        <h3 className="text-lg font-semibold text-gray-800 leading-relaxed">
                          {classificationResult.title}
                        </h3>
                      </div>
                      <div>
                        <p className="text-sm text-green-700 font-medium mb-3">Classification Labels:</p>
                        <div className="flex flex-wrap gap-3">
                          {classificationResult.labels.map((label, index) => (
                            <Badge
                              key={index}
                              className="px-4 py-2 text-sm font-medium bg-gradient-to-r from-blue-100 to-teal-100 text-blue-800 border border-blue-200 hover:from-blue-200 hover:to-teal-200 transition-colors"
                            >
                              {label}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ) : null}
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  )
}
