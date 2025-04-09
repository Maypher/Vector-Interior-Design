<script lang="ts">
	import '../app.css';
	import { getI18n, setI18n } from '$lib/i18n';
	import type { PageData } from './$types';
	import type { Snippet } from 'svelte';

	const { children, data }: { data: PageData; children: Snippet } = $props();

	setI18n(data.i18n);
</script>

{@render children()}
