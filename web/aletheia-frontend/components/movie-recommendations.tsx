"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Film } from "lucide-react"
import Image from "next/image"

interface Movie {
  title: string
  genre: string
  description: string
  banner: string
}

interface MovieRecommendationsProps {
  recommendations: Movie[]
  onReset: () => void
}

export function MovieRecommendations({ recommendations, onReset }: MovieRecommendationsProps) {
  return (
    <div className="max-w-6xl mx-auto animate-in fade-in duration-500">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold mb-2 flex items-center gap-2">
            <Film className="w-8 h-8 text-primary" />
            Your Recommendations
          </h2>
          <p className="text-muted-foreground">Based on your taste, we think you'll love these</p>
        </div>
        <Button
          onClick={onReset}
          variant="outline"
          className="gap-2 bg-transparent hover:bg-primary/10 hover:text-primary hover:border-primary transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Start Over
        </Button>
      </div>

      <div className="grid gap-6">
        {recommendations.map((movie, index) => (
          <Card
            key={index}
            className="overflow-hidden bg-card border-border hover:border-primary/50 transition-all duration-300 hover:shadow-xl hover:shadow-primary/10 group"
            style={{
              animationDelay: `${index * 0.1}s`,
            }}
          >
            <div className="md:flex">
              <div className="relative md:w-80 h-48 md:h-auto flex-shrink-0 overflow-hidden bg-muted">
                <Image
                  src={movie.banner || "/placeholder.svg"}
                  alt={movie.title}
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-card/80 to-transparent md:bg-gradient-to-r" />
              </div>

              <div className="p-6 flex-1">
                <div className="flex items-start justify-between gap-4 mb-3">
                  <h3 className="text-2xl font-bold text-balance">{movie.title}</h3>
                  <span className="px-3 py-1 bg-primary text-primary-foreground text-sm font-medium rounded-full whitespace-nowrap">
                    {movie.genre}
                  </span>
                </div>

                <p className="text-muted-foreground leading-relaxed">{movie.description}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
