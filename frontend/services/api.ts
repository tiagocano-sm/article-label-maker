export interface ClassifyArticleRequest {
  title: string
  abstract: string
}

export interface ClassifyArticleResponse {
  title: string
  labels: string[]
}

export interface ClassifyCSVResponse {
  message: string
  processed_rows: number
  output_filename: string
}

export class ApiService {
  private static baseUrl = "/api"

  static async classifyArticle(data: ClassifyArticleRequest): Promise<ClassifyArticleResponse> {
    const response = await fetch(`${this.baseUrl}/classify_article`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      throw new Error(`Failed to classify article: ${response.statusText}`)
    }

    return response.json()
  }

  static async classifyArticlesInCSV(file: File): Promise<ClassifyCSVResponse> {
    console.log("Starting CSV upload...", { fileName: file.name, fileSize: file.size })
    
    const formData = new FormData()
    formData.append("file", file)

    console.log("Sending request to:", `${this.baseUrl}/classify_articles_in_csv`)
    
    const response = await fetch(`${this.baseUrl}/classify_articles_in_csv`, {
      method: "POST",
      body: formData,
    })

    console.log("Response status:", response.status, response.statusText)

    if (!response.ok) {
      const errorText = await response.text()
      console.error("Response error:", errorText)
      throw new Error(`Failed to process CSV: ${response.statusText} - ${errorText}`)
    }

    const result = await response.json()
    console.log("CSV processing result:", result)
    return result
  }

  static async downloadProcessedCSV(filename: string): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/download/${filename}`, {
      method: "GET",
    })

    if (!response.ok) {
      throw new Error(`Failed to download file: ${response.statusText}`)
    }

    return response.blob()
  }
}
