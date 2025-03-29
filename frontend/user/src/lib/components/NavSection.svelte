<script lang="ts">
	import { getI18n } from '$lib/i18n';
	import symbol from '$lib/images/symbol.svg';
	import '$lib/styles/markdown.css';
	import { onMount } from 'svelte';

	interface Props {
		image: any;
	}

	const i18n = getI18n();

	const { image }: Props = $props();

	let imgLoaded: boolean = $state(false);

	onMount(() => {
		// This entire setup doesn't work in Chrome mobile app for some reason
		const pencilObserver = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						const pencil = document.getElementById('pencil');
						if (pencil) {
							pencil.classList.add('pencil-animate');
							pencilObserver.unobserve(entry.target);
						}
					}
				});
			},
			{
				threshold: 0.6
			}
		);

		const pencil = document.getElementById('nav');
		if (pencil) pencilObserver.observe(pencil);
	});
</script>

<div
	class="lg:min-h-120 mt-20 flex w-full flex-col gap-y-10 overflow-hidden lg:mt-0 lg:h-[70svh] lg:flex-row lg:items-center lg:justify-evenly"
	id="nav"
	style={`background-color: ${image.mainImageConfig.bgColor};`}
>
	<img
		src={image.imageUrl}
		alt={image.altText}
		class="lg:max-w-2/3 max-h-full max-w-full object-contain"
		class:hidden={!imgLoaded}
		style={`height: calc(${image.mainImageConfig.imageSize} / 100 * 100%);`}
		onload={() => (imgLoaded = true)}
	/>
	<div
		class="skeleton w-2/3"
		class:hidden={imgLoaded}
		style={`height: calc(${image.mainImageConfig.imageSize} / 100 * 100%);`}
	></div>
	<ul
		class="text-vector-cream relative flex items-center justify-center gap-5 p-5 text-xl lg:h-4/5"
	>
		<li class="hover-link font-Nexa relative top-0 z-10 h-fit w-fit">
			<a href={`${$i18n.language}/esculturas/`} class="text-vector-cream">
				{$i18n.t('sculptures')}
			</a>
		</li>
		<div class="h-92 flex w-[2px] flex-col items-center overflow-visible" id="pencil">
			<img src={symbol} alt="V" class="min-h-20 min-w-20" />
			<div class="bg-vector-orange relative bottom-3 h-2/3 w-px"></div>
		</div>
		<li class="hover-link font-Nexa relative bottom-10 z-10 w-fit after:relative after:top-1">
			<a href={`/${$i18n.language}/proyectos/`} class="text-vector-cream">
				{$i18n.t('projects')}
			</a>
		</li>
	</ul>
</div>

<style>
	#pencil {
		position: relative;
		top: 120%;
	}

	:global .pencil-animate {
		position: relative;
		animation: pencil-draw 2s ease-in-out forwards;
	}

	@keyframes pencil-draw {
		to {
			top: 0%;
		}
	}
</style>
