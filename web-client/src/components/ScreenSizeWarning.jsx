import { cn } from "../lib/utils"

export default function ScreenSizeWarning() {
    return (
        <div className={cn(
            "fixed inset-0 z-50 flex min-h-screen w-full items-center justify-center",
            "bg-background p-8 text-center"
        )}>
            <div className="max-w-md space-y-4">
                <h1 className="text-2xl font-bold">Mobile View Required</h1>
                <p className="text-muted-foreground">
                    ScribeX is designed to be used on mobile devices for students. Please switch to a phone or tablet to continue.
                </p>
                <div className="text-sm text-muted-foreground">
                    Recommended maximum width: 430px (portrait phone)
                </div>
            </div>
        </div>
    )
} 