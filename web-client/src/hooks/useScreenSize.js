import { useState, useEffect } from 'react'

const MAX_STUDENT_WIDTH = 430 // Max width for portrait phone view

export function useScreenSize() {
    const [isScreenTooLarge, setIsScreenTooLarge] = useState(false)

    useEffect(() => {
        const checkScreenSize = () => {
            setIsScreenTooLarge(window.innerWidth > MAX_STUDENT_WIDTH)
        }

        // Check on mount
        checkScreenSize()

        // Check on resize
        window.addEventListener('resize', checkScreenSize)
        return () => window.removeEventListener('resize', checkScreenSize)
    }, [])

    return { isScreenTooLarge }
} 