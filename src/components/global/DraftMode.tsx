'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

export const DraftMode = () => {
  const router = useRouter()
  const [disabling, setDisabling] = useState(false)

  return (
    <div
      className={`fixed bottom-5 left-5 p-5 text-white bg-vector-grey/10 backdrop-blur-sm flex gap-x-2 ${disabling ? 'cursor-wait' : ''}`}
    >
      <button
        type="button"
        className="text-red-400 cursor-pointer"
        disabled={disabling}
        onClick={async () => {
          setDisabling(true)
          await fetch('/draft/disable')
          router.refresh()
        }}
      >
        X
      </button>
      <p>Modo Borrador activo</p>
    </div>
  )
}
