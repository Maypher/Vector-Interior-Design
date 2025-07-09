'use client'

import { TextFieldClientProps } from 'payload'
import { FieldLabel, FieldDescription, FieldType } from '@payloadcms/ui'
import { useField } from '@payloadcms/ui'

const defaultColors = ['#101214', '#1c2025']

export default function ColorSelect(props: TextFieldClientProps) {
  const { path, field } = props
  const { value, setValue }: FieldType<string> = useField({ path })

  return (
    <div>
      <FieldLabel
        path={path}
        required={field.required}
        label={field.label}
        localized={field.localized}
      />
      <ul
        style={{
          listStyle: 'none',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          backgroundColor: 'lightgray',
          width: 'fit-content',
          padding: '0.5rem',
        }}
      >
        {defaultColors.map((color) => (
          <li key={color}>
            <button
              type="button"
              role="color-select"
              key={`${color}-button`}
              className={`border-vector-black ${value === color && 'border-4'}`}
              style={{
                backgroundColor: color,
                width: '4rem',
                height: '4rem',
                borderRadius: '50px',
                borderColor: 'gray',
                borderWidth: value === color ? '4px' : '0',
                color: 'white',
              }}
              onClick={() => setValue(color)}
              aria-label={color}
            ></button>
          </li>
        ))}
        <li>
          <input type="color" onChange={(e) => setValue(e.currentTarget.value)} />
        </li>
      </ul>
      <FieldDescription path={path} description={field.admin?.description} />
    </div>
  )
}
