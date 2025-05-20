import { DefaultNodeTypes } from '@payloadcms/richtext-lexical'
import { JSXConvertersFunction } from '@payloadcms/richtext-lexical/react'

/// Custom converter that changes all header tags to `<p class="level-#">` to not confuse screen readers
/// and search engines.
const headersConverter: JSXConvertersFunction<DefaultNodeTypes> = ({ defaultConverters }) => ({
  ...defaultConverters,
  // Override the default upload converter
  heading: ({ node, nodesToJSX }) => {
    const headerLevel = node.tag.at(-1)
    return <p className={`level level-${headerLevel}`}>{nodesToJSX({ nodes: node.children })}</p>
  },
})

export default headersConverter
