<script lang="ts">
	import { websiteUrl } from '$lib/utilities/constants';

	interface Props {
		title: string;
		description: string;
		url: string;
		alternateEs: string;
		alternateEn: string;
		ogTitle: string;
		ogDescription: string;
		imageUrl?: string;
	}

	let {
		url,
		title,
		alternateEn,
		alternateEs,
		ogTitle,
		description,
		imageUrl,
		ogDescription
	}: Props = $props();

	// Doing this to remove all markdown syntax in description
	ogDescription = ogDescription
		.replace(/(\*\*|__)(.*?)\1/g, '$2') // Bold (**text** or __text__)
		.replace(/(`{1,3})(.*?)\1/g, '$2') // Inline code (`code` or ```code```)
		.replace(/!\[.*?\]\(.*?\)/g, '') // Images (![alt](url))
		.replace(/\[(.*?)\]\(.*?\)/g, '$1') // Links ([text](url))
		.replace(/^> /gm, '') // Blockquotes (> quote)
		.replace(/^#{1,6}/gm, '') // Headings (# H1, ## H2, etc.)
		.replace(/^\* |\d+\.\s/gm, '') // Lists (- item, 1. item)
		.replace(/~~(.*?)~~/g, '$1') // Strikethrough (~~text~~)
		.replace(/`/g, '') // Inline backticks (`code`)
		.replace(/---/g, '') // Horizontal rules (---)
		.replace(/\|.*?\|/g, '') // Tables (| col1 | col2 |)
		.trim();
</script>

<svelte:head>
	<title>{title}</title>

	<meta name="description" content={description} />

	<link rel="alternate" hreflang="en" href={alternateEn} />
	<link rel="alternate" hreflang="es" href={alternateEs} />

	<!-- Facebook Meta Tags -->
	<meta property="og:url" content={url} />
	<meta property="og:type" content="website" />
	<meta property="og:title" content={ogTitle} />
	<meta property="og:description" content={ogDescription} />
	<meta property="og:image" content={imageUrl} />

	<!-- Twitter Meta Tags -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta property="twitter:domain" content={websiteUrl.replace('https://', '')} />
	<meta property="twitter:url" content={url} />
	<meta name="twitter:title" content={ogTitle} />
	<meta name="twitter:description" content={ogDescription} />
	<meta name="twitter:image" content={imageUrl} />
</svelte:head>
