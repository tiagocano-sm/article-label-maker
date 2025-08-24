"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { BarChart3 } from "lucide-react"

interface MetricsData {
  overall_metrics: {
    micro_f1_score: number
    precision: number
    overall_accuracy: number
    total_samples: number
    correct_predictions: number
    incorrect_predictions: number
  }
  overall_confusion_matrix: {
    correct_predictions: number
    false_positives: number
    false_negatives: number
    total_predictions: number
    accuracy: number
  }
  labels: string[]
  last_updated: string
  has_data: boolean
}

export function Dashboard() {
  const [metricsData, setMetricsData] = useState<MetricsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchMetrics()
  }, [])

  const fetchMetrics = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/dashboard')
      if (!response.ok) {
        throw new Error('Failed to fetch metrics')
      }
      const data = await response.json()
      setMetricsData(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(2)}%`
  }

  const getMetricColor = (value: number) => {
    if (value >= 0.8) return "text-green-600"
    if (value >= 0.6) return "text-yellow-600"
    return "text-red-600"
  }

  const getMetricBadgeVariant = (value: number) => {
    if (value >= 0.8) return "default" as const
    if (value >= 0.6) return "secondary" as const
    return "destructive" as const
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Loading metrics...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-600">Error: {error}</div>
      </div>
    )
  }

  if (!metricsData || !metricsData.has_data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">No metrics data available</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Model Performance Dashboard</h1>
          <p className="text-gray-600">
            Last updated: {new Date(metricsData.last_updated).toLocaleString()}
          </p>
        </div>
        <Badge variant="outline">
          {metricsData.overall_metrics.total_samples.toLocaleString()} samples
        </Badge>
      </div>

      {/* Overall Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Micro F1-Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              <span className={getMetricColor(metricsData.overall_metrics.micro_f1_score)}>
                {formatPercentage(metricsData.overall_metrics.micro_f1_score)}
              </span>
            </div>
            <Progress value={metricsData.overall_metrics.micro_f1_score * 100} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Precision</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              <span className={getMetricColor(metricsData.overall_metrics.precision)}>
                {formatPercentage(metricsData.overall_metrics.precision)}
              </span>
            </div>
            <Progress value={metricsData.overall_metrics.precision * 100} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Overall Accuracy</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              <span className={getMetricColor(metricsData.overall_metrics.overall_accuracy)}>
                {formatPercentage(metricsData.overall_metrics.overall_accuracy)}
              </span>
            </div>
            <Progress value={metricsData.overall_metrics.overall_accuracy * 100} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Correct Predictions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {metricsData.overall_metrics.correct_predictions.toLocaleString()}
            </div>
            <p className="text-xs text-gray-600 mt-1">
              Out of {metricsData.overall_metrics.total_samples.toLocaleString()} total
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Confusion Matrix Section */}
      <Card className="shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <BarChart3 className="w-6 h-6 text-blue-600" />
            Model Performance Details
          </CardTitle>
          <CardDescription className="text-lg text-gray-700">
            Detailed breakdown of model predictions and performance metrics
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-6">

          <div className="space-y-6">
            {/* Summary Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
                <div className="text-2xl font-bold text-green-600">
                  {metricsData.overall_confusion_matrix.correct_predictions.toLocaleString()}
                </div>
                <div className="text-sm text-green-700 font-medium">Correct Predictions</div>
                <div className="text-xs text-green-600">
                  {formatPercentage(metricsData.overall_confusion_matrix.accuracy)}
                </div>
              </div>
              
              <div className="text-center p-4 bg-red-50 rounded-lg border border-red-200">
                <div className="text-2xl font-bold text-red-600">
                  {metricsData.overall_confusion_matrix.false_positives.toLocaleString()}
                </div>
                <div className="text-sm text-red-700 font-medium">False Positives</div>
                <div className="text-xs text-red-600">
                  {formatPercentage(metricsData.overall_confusion_matrix.false_positives / metricsData.overall_confusion_matrix.total_predictions)}
                </div>
              </div>
              
              <div className="text-center p-4 bg-orange-50 rounded-lg border border-orange-200">
                <div className="text-2xl font-bold text-orange-600">
                  {metricsData.overall_confusion_matrix.false_negatives.toLocaleString()}
                </div>
                <div className="text-sm text-orange-700 font-medium">False Negatives</div>
                <div className="text-xs text-orange-600">
                  {formatPercentage(metricsData.overall_confusion_matrix.false_negatives / metricsData.overall_confusion_matrix.total_predictions)}
                </div>
              </div>
            </div>

            {/* Visual Matrix */}
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">Prediction Matrix</h3>
              <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
                <div className="text-center p-4 bg-green-100 rounded-lg border-2 border-green-300">
                  <div className="text-xl font-bold text-green-700">
                    {metricsData.overall_confusion_matrix.correct_predictions.toLocaleString()}
                  </div>
                  <div className="text-sm text-green-600 font-medium">Correct</div>
                </div>
                <div className="text-center p-4 bg-red-100 rounded-lg border-2 border-red-300">
                  <div className="text-xl font-bold text-red-700">
                    {(metricsData.overall_confusion_matrix.false_positives + metricsData.overall_confusion_matrix.false_negatives).toLocaleString()}
                  </div>
                  <div className="text-sm text-red-600 font-medium">Incorrect</div>
                </div>
              </div>
              
              <div className="mt-4 text-center">
                <div className="text-sm text-gray-600">
                  Total Predictions: {metricsData.overall_confusion_matrix.total_predictions.toLocaleString()}
                </div>
                <div className="text-lg font-semibold text-gray-800 mt-1">
                  Overall Accuracy: {formatPercentage(metricsData.overall_confusion_matrix.accuracy)}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
