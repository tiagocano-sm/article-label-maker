export interface ClassifyArticleRequest {
  title: string
  abstract: string
}

export interface ClassifyArticleResponse {
  title: string
  labels: string[]
}

export interface ClassifyCSVResponse {
  blob: Blob
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
    const formData = new FormData()
    formData.append("file", file)

    const response = await fetch(`${this.baseUrl}/classify_articles_in_csv`, {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Failed to process CSV: ${response.statusText}`)
    }

    const blob = await response.blob()
    return { blob }
  }
}
