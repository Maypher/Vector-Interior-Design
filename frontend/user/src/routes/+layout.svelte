<script lang="ts">
	import '../app.css';
	import { setI18n } from '$lib/i18n';
	import type { Snippet } from 'svelte';
	import { afterNavigate } from '$app/navigation';
	import textBalancePolyfill from '$lib/text-balance-polyfill';

	const { children, data }: { data: any; children: Snippet } = $props();

	setI18n(data.i18n);

	// Using afterNavigate because using onMount only runs it on page load
	// so when navigating text doesn't get updated
	afterNavigate(() => textBalancePolyfill());
</script>

{@render children()}
