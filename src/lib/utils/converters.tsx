import { JSXConvertersFunction } from '@payloadcms/richtext-lexical/react'
import { DefaultNodeTypes } from '@payloadcms/richtext-lexical'

type NodeTypes = DefaultNodeTypes

// Using a converter to change headings to p tags since they are used for sizes rather than content.
export const headerConverter: JSXConvertersFunction<NodeTypes> = ({ defaultConverters }) => ({
  ...defaultConverters,
  // Override the default upload converter
  heading: ({ node, nodesToJSX }) => {
    const level = node.tag.charAt(node.tag.length - 1)
    return <p className={`level-${level}`}>{nodesToJSX({ nodes: [node] })}</p>
  },
})
