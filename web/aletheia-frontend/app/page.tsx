"use client"

import { useState } from "react"
import { MovieSelector } from "@/components/movie-selector"
import { MovieRecommendations } from "@/components/movie-recommendations"
import { FilmReelLoader } from "@/components/film-reel-loader"
import { Film } from "lucide-react"

export default function Home() {
  const [selectedMovies, setSelectedMovies] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [recommendations, setRecommendations] = useState<any[]>([])
  const [showRecommendations, setShowRecommendations] = useState(false)

  const handleGetRecommendations = async () => {
    setIsLoading(true)
    setShowRecommendations(false)

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 3000))

    // API call to node
    // await fetch("/api/recommend", {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({
    //     item_ids: selectedMovies,
    //     k: 5,
    //   }),
    // });

    // Mock recommendations
    const mockRecommendations = [
      {
        title: "Blade Runner 2049",
        genre: "Sci-Fi, Thriller",
        description:
          "A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard.",
        banner: "/blade-runner-2049-dystopian-cityscape.jpg",
      },
      {
        title: "Arrival",
        genre: "Sci-Fi, Drama",
        description:
          "A linguist works with the military to communicate with alien lifeforms after mysterious spacecraft appear around the world.",
        banner: "/arrival-alien-spaceship-atmosphere.jpg",
      },
      {
        title: "The Prestige",
        genre: "Mystery, Thriller",
        description:
          "Two stage magicians engage in competitive one-upmanship in an attempt to create the ultimate stage illusion.",
        banner: "/the-prestige-magic-victorian-era.jpg",
      },
      {
        title: "Mad Max: Fury Road",
        genre: "Action, Adventure",
        description:
          "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland.",
        banner: "/mad-max-fury-road-desert-action.jpg",
      },
      {
        title: "Dunkirk",
        genre: "War, Drama",
        description:
          "Allied soldiers from Belgium, the British Commonwealth and France are surrounded by the German Army and evacuated during a fierce battle.",
        banner: "/dunkirk-war-beach-evacuation.jpg",
      },
    ]

    setRecommendations(mockRecommendations)
    setIsLoading(false)
    setShowRecommendations(true)
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Film className="w-10 h-10 text-primary" />
            <h1 className="text-5xl font-bold text-balance">Aletheia</h1>
          </div>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto text-balance">
            Select 5 movies you love and discover your next favorite film
          </p>
        </div>

        {!showRecommendations ? (
          <>
            <MovieSelector
              selectedMovies={selectedMovies}
              onSelectionChange={setSelectedMovies}
              onGetRecommendations={handleGetRecommendations}
            />

            {isLoading && <FilmReelLoader />}
          </>
        ) : (
          <MovieRecommendations
            recommendations={recommendations}
            onReset={() => {
              setShowRecommendations(false)
              setSelectedMovies([])
              setRecommendations([])
            }}
          />
        )}
      </div>
    </main>
  )
}
