<script lang="ts">
	import { page } from '$app/state';
	import { getI18n } from '$lib/i18n';

	const i18n = getI18n();
</script>

<svelte:head>
	<title>{$i18n.language === 'es' ? 'Página no encontrada' : 'Page not found.'}</title>
	<meta name="robots" content="noindex, nofollow" />
</svelte:head>

<div class="flex h-screen w-screen flex-col items-center justify-center gap-5 text-4xl text-white">
	<h1 class="font-Noopla text-vector-orange text-[20rem]" style="line-height: 0.8;">X</h1>
	<a href={`/${$i18n.language}/`} class="font-Noopla">
		<span id="arrow">&lt;-</span>
		{#if page.status === 404}
			{$i18n.language === 'es' ? 'Página no encontrada' : 'Page not found'}
		{:else}
			{page.error?.message}
		{/if}
	</a>
</div>

<style>
	#arrow {
		position: relative;
		animation: move 1s ease-in-out infinite both;
	}

	@keyframes move {
		0% {
			right: 0;
		}
		50% {
			right: 2%;
		}
		100% {
			right: 0;
		}
	}
</style>
