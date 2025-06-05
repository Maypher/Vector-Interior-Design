'use client'

import Image from 'next/image'
import logo from '@public/images/logo.svg'
import LanguageSelect from './LanguageSelect'
import { useState, useEffect, useRef } from 'react'
import { Link } from '@/i18n/navigation'
import { useTranslations } from 'next-intl'

export default function Header() {
  const [menuOpen, setMenuOpen] = useState<boolean>(false)
  const t = useTranslations('NavBar')
  const menuElement = useRef<HTMLDivElement>(null)
  const menuBtn = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    // If the menu was opened then add an event listener to close it when clicking outside it
    if (menuOpen) {
      const handleClickOutside = (event: MouseEvent) => {
        // Type the event as MouseEvent
        const clickedElement = event.target as Node // Type target as Node

        // Now menuRef.current is known to be an HTMLDivElement, so .contains() is safe
        const clickInsideMenu = menuElement.current?.contains(clickedElement)
        const clickedUrl = clickedElement.nodeName === 'A'
        const clickedBtn = menuBtn.current === clickedElement

        if ((!clickInsideMenu || clickedUrl) && !clickedBtn) setMenuOpen(false)
      }

      // Using setTimeout with delay 0 because since the 'click' event
      // triggers with the click to open the menu this delays it to the next
      // cycle which is enough to not trigger it automatically.
      const timerId = setTimeout(() => {
        document.addEventListener('mousedown', handleClickOutside)
      }, 0)

      return () => {
        clearTimeout(timerId)
        document.removeEventListener('mousedown', handleClickOutside)
      }
    }
  }, [menuOpen])

  return (
    <div>
      <header className="h-22 bg-vector-cream px-10 py-5 flex items-center justify-between">
        <Image src={logo} alt="Vector: Interior Design" className="h-full w-fit" />
        <div className="hidden xl:block">
          <LanguageSelect />
        </div>
        <button
          type="button"
          className={`text-vector-black flex flex-col gap-y-2 transition-transform xl:hidden ${menuOpen ? '-rotate-90' : ''}`}
          onClick={() => {
            console.log('Clicked')
            setMenuOpen((prevValue) => !prevValue)
          }}
          ref={menuBtn}
        >
          <div className="w-7 h-1 rounded-sm bg-vector-black"></div>
          <div className="w-7 h-1 rounded-sm bg-vector-black"></div>
          <div className="w-7 h-1 rounded-sm bg-vector-black"></div>
        </button>
      </header>
      <div
        className={`bg-vector-black transition-all max-h-0 overflow-clip ${menuOpen ? 'max-h-200' : ''}`}
        id="menu"
        ref={menuElement}
      >
        <ul className="text-right [&_li]:p-2" style={{ letterSpacing: '0.05rem' }}>
          <li>
            <LanguageSelect />
          </li>
          <li>
            <Link href="#aboutUs">{t('aboutUs')}</Link>
          </li>
          <li>
            <Link href="/projects">{t('projects')}</Link>
          </li>
          <li>
            <Link href="/sculptures">{t('sculptures')}</Link>
          </li>
          <li>
            <Link href="#contact">{t('contact')}</Link>
          </li>
        </ul>
      </div>
    </div>
  )
}
