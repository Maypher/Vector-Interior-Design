'use client'

import '@styles/scrollingText.scss'

import { useEffect, useRef, useState } from 'react'

export default function ScrollingText({
  text,
  color,
}: {
  text: string | null | undefined
  color: string
}) {
  const textElement = useRef<HTMLSpanElement>(null)
  const textContainer = useRef<HTMLDivElement>(null)

  const [amountToFill, setAmountToFill] = useState(1)
  const [textWidth, setTextWidth] = useState(0)

  useEffect(() => {
    function setupScroll() {
      if (!textElement.current || !textContainer.current) return

      const textStyles = getComputedStyle(textElement.current)
      const textWidth =
        textElement.current.getBoundingClientRect().width +
        parseFloat(textStyles.marginInline.replace('px', '')) * 2
      const screenWidth = window.screen.width

      // Adding plus one to have a hidden one on the left edge
      // of the screen so it scrolls into view
      setAmountToFill(Math.ceil(screenWidth / textWidth) + 1)
      setTextWidth(textWidth)

      textContainer.current.style.setProperty('--scroll-amount', `${textWidth}px`)
    }

    setupScroll()

    document.addEventListener('resize', setupScroll)

    return () => document.removeEventListener('resize', setupScroll)
  }, [textElement, textContainer, text])

  return (
    <div
      className="text-2xl w-svw text-nowrap overflow-x-clip whitespace-nowrap"
      style={{ color }}
      ref={textContainer}
    >
      {[...new Array(amountToFill)].map((_, i) => (
        <span
          ref={textElement}
          key={i}
          className={`relative mx-25 w-fit ${amountToFill > 1 ? 'scroll-text' : ''} whitespace-nowrap`}
          style={{ right: `${textWidth}px` }}
        >
          {text}
        </span>
      ))}
    </div>
  )
}
