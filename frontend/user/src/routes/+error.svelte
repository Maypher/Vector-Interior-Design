<script lang="ts">
	import { page } from '$app/state';
	import { getI18n } from '$lib/i18n';

	const i18n = getI18n();

	const isSpanish = $i18n.language === 'es';
</script>

<svelte:head>
	<title>{$i18n.language === 'es' ? 'Página no encontrada' : 'Page not found'}</title>
	<meta name="robots" content="noindex, nofollow" />
</svelte:head>

<div class="flex h-screen w-screen flex-col items-center justify-center gap-5 text-4xl text-white">
	<h1 class="font-Noopla text-vector-orange text-[20rem]" style="line-height: 0.8;">X</h1>
	<a
		href={`/${$i18n.language}/`}
		class="font-Noopla text-center"
		class:pointer-events-none={page.status === 403}
	>
		{#if page.status === 404}
			<span id="arrow">&lt;-</span>
			{isSpanish ? 'Página no encontrada' : 'Page not found'}
		{:else if page.status === 502}
			{isSpanish
				? 'Servidor temporalmente fuera de servicio. Por favor intentar de nuevo más tarde'
				: 'Server temporarily down. Please try again later.'}
		{:else if page.status === 403}
			{isSpanish
				? 'Página bajo construcción. Revisar de nuevo después.'
				: 'Page under construction. Check back again later.'}
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
