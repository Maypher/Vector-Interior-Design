<script lang="ts">
	import '../app.css';
	import { setupI18n, setI18n } from '$lib/i18n';
	import { getI18n } from '$lib/i18n';
	import type { PageData } from './$types';
	import type { Snippet } from 'svelte';

	const { children, data }: { data: PageData; children: Snippet } = $props();

	const preferredLang = data.selectedLanguage;

	setI18n(setupI18n());
	const i18n = getI18n();

	$i18n.changeLanguage(preferredLang);
</script>

<svelte:head>
	<meta lang={preferredLang} />
</svelte:head>

{@render children()}
