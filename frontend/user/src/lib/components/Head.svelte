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

	const { url, title, alternateEn, alternateEs, ogTitle, description, imageUrl }: Props = $props();
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
	<meta property="og:description" content={description} />
	<meta property="og:image" content={imageUrl} />

	<!-- Twitter Meta Tags -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta property="twitter:domain" content={websiteUrl.replace('https://', '')} />
	<meta property="twitter:url" content={url} />
	<meta name="twitter:title" content={ogTitle} />
	<meta name="twitter:description" content={description} />
	<meta name="twitter:image" content={imageUrl} />
</svelte:head>
