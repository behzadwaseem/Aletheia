"use client"

export function FilmReelLoader() {
  return (
    <div className="fixed inset-0 bg-background/95 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="relative">
        <div className="relative border-shimmer-wrapper-pulse-1">
          <div className="border-shimmer-wrapper-pulse-2">
            <div className="w-48 h-64 rounded-md">
              <div className="w-full h-full overflow-hidden relative rounded-md border border-border/50 bg-background">
                {/* Film strip container */}
                <div className="film-strip-roll absolute inset-0">
                  {[...Array(8)].map((_, i) => (
                    <div key={i} className="film-frame relative">
                      <div className="absolute left-3 top-0 bottom-0 flex flex-col justify-around">
                        {[...Array(3)].map((_, j) => (
                          <div key={j} className="w-1.5 h-1.5 rounded-full bg-muted-foreground/30" />
                        ))}
                      </div>
                      <div className="absolute right-3 top-0 bottom-0 flex flex-col justify-around">
                        {[...Array(3)].map((_, j) => (
                          <div key={j} className="w-1.5 h-1.5 rounded-full bg-muted-foreground/30" />
                        ))}
                      </div>

                      <div className="mx-7 h-full border-y border-border/30 bg-muted/20" />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-muted-foreground">Finding recommendations</p>
        </div>
      </div>
    </div>
  )
}
