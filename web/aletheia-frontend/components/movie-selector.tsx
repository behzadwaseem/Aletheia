"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { X, Search, Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

const POPULAR_MOVIES = [
  "Inception",
  "The Shawshank Redemption",
  "The Dark Knight",
  "Pulp Fiction",
  "Forrest Gump",
  "The Matrix",
  "Interstellar",
  "Fight Club",
  "Goodfellas",
  "The Godfather",
  "Parasite",
  "Spirited Away",
  "Whiplash",
  "The Grand Budapest Hotel",
  "La La Land",
  "Eternal Sunshine",
  "Her",
  "Drive",
  "Moonlight",
  "The Social Network",
]

interface MovieSelectorProps {
  selectedMovies: string[]
  onSelectionChange: (movies: string[]) => void
  onGetRecommendations: () => void
}

export function MovieSelector({ selectedMovies, onSelectionChange, onGetRecommendations }: MovieSelectorProps) {
  const [searchQuery, setSearchQuery] = useState("")

  const filteredMovies = POPULAR_MOVIES.filter((movie) => movie.toLowerCase().includes(searchQuery.toLowerCase()))

  const toggleMovie = (movie: string) => {
    if (selectedMovies.includes(movie)) {
      onSelectionChange(selectedMovies.filter((m) => m !== movie))
    } else if (selectedMovies.length < 5) {
      onSelectionChange([...selectedMovies, movie])
    }
  }

  const isSelected = (movie: string) => selectedMovies.includes(movie)
  const canGetRecommendations = selectedMovies.length === 5

  return (
    <div className="max-w-5xl mx-auto">
      <Card className="p-6 bg-card border-border">
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-4">
            <h2 className="text-2xl font-semibold">Select Your Favorites</h2>
            <span className="text-sm text-muted-foreground">({selectedMovies.length}/5)</span>
          </div>

          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search for movies..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-background border-border"
            />
          </div>
        </div>

        {selectedMovies.length > 0 && (
          <div className="mb-6 p-4 bg-secondary/50 rounded-lg border border-border">
            <h3 className="text-sm font-medium text-muted-foreground mb-3">Your Selection</h3>
            <div className="flex flex-wrap gap-2">
              {selectedMovies.map((movie) => (
                <div
                  key={movie}
                  className="flex items-center gap-2 px-3 py-1.5 bg-primary text-primary-foreground rounded-full text-sm font-medium"
                >
                  {movie}
                  <button
                    onClick={() => toggleMovie(movie)}
                    className="hover:bg-primary-foreground/20 rounded-full p-0.5 transition-colors"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mb-6 max-h-96 overflow-y-auto pr-2">
          {filteredMovies.map((movie) => (
            <button
              key={movie}
              onClick={() => toggleMovie(movie)}
              disabled={!isSelected(movie) && selectedMovies.length >= 5}
              className={cn(
                "px-4 py-3 rounded-lg text-left transition-all duration-200 font-medium",
                "border-2 hover:scale-[1.02]",
                isSelected(movie)
                  ? "bg-primary border-primary text-primary-foreground shadow-lg shadow-primary/20"
                  : "bg-card border-border hover:border-primary/50 hover:bg-card/80",
                !isSelected(movie) && selectedMovies.length >= 5 && "opacity-50 cursor-not-allowed",
              )}
            >
              {movie}
            </button>
          ))}
        </div>

        <Button
          onClick={onGetRecommendations}
          disabled={!canGetRecommendations}
          size="lg"
          className="w-full text-lg font-semibold gap-2 bg-primary hover:bg-primary/90"
        >
          <Sparkles className="w-5 h-5" />
          Get Recommendations
        </Button>
      </Card>
    </div>
  )
}
