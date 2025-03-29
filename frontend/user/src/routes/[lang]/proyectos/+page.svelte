<script lang="ts">
	import { websiteUrl } from '$lib/utilities/constants';
	import Head from '$lib/components/Head.svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';
	import Glide, { Controls, Swipe } from '@glidejs/glide/dist/glide.modular.esm.js';
	import '@glidejs/glide/dist/css/glide.core.min.css';
	import logoWhite from '$lib/images/logo white.svg';

	const { data }: { data: PageData } = $props();
	const projects: any[] = data.projects;

	onMount(() => {
		// Mobile arrow
		const arrow = document.getElementById('arrow')!;
		arrow.addEventListener('transitionend', (e: TransitionEvent) => {
			arrow.classList.add('animate');
			e.target?.removeEventListener('transitionend', null);
		});

		setTimeout(() => {
			arrow.classList.add('showing');
		}, 500);

		const arrowLimit = document.getElementById('arrowLimit');

		if (arrowLimit) {
			const observer = new IntersectionObserver((entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						if (arrow.classList.contains('showing')) {
							arrow.classList.remove('showing');
							arrow.classList.remove('hiding');
							setTimeout(() => arrow.remove(), 100);
						} else arrow.remove();

						observer.disconnect();
					}
				});
			});

			observer.observe(arrowLimit);
		}

		new Glide('#carousel', {
			type: 'slider',
			perView: 3,
			bound: true
		}).mount({ Controls, Swipe });
	});

	const i18n = getI18n();
</script>

<Head
	title={$i18n.language === 'es' ? 'Proyectos' : 'Projects'}
	description={$i18n.language === 'es' ? '' : ''}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en/proyectos`}
	alternateEs={`${websiteUrl}/es/proyectos`}
	ogTitle={$i18n.language === 'es'
		? 'Vector: Interior Design (Proyectos)'
		: 'Vector: Interior Design (Projects)'}
	ogDescription={$i18n.language === 'es' ? '' : ''}
	imageUrl={projects.at(0).thumbnail.imageUrl}
/>

<ul class="header-screen bg-vector-grey snap-y snap-mandatory overflow-y-scroll lg:hidden">
	{#each projects as project, i (project.id)}
		{#if project.thumbnail}
			<li class="flex h-full snap-center items-center justify-center text-white" id={project.id}>
				<div class="flex h-full flex-col justify-center">
					<a
						href={`/${$i18n.language}/proyectos/${project.id}`}
						class="flex h-3/4 flex-col justify-center gap-6 px-8"
					>
						<figure class="h-full">
							<img
								src={project.thumbnail.imageUrl}
								alt={project.thumbnail.altText}
								class="h-full object-cover"
							/>
							<figcaption class="my-2">
								<p class="font-Nexa">{project.name}</p>
							</figcaption>
						</figure>
					</a>
				</div>
				{#if i === 1}
					<div id="arrowLimit" inert></div>
				{/if}
			</li>
		{/if}
		{#if i === 0}
			<div id="arrow" inert></div>
		{/if}
	{/each}
</ul>

<div id="carousel" class="hidden lg:block">
	<div
		class="glide__track bg-vector-grey header-screen relative flex flex-col pb-10"
		data-glide-el="track"
	>
		<ul class=" glide__slides h-full grow-0">
			{#each projects as project, i (project.id)}
				<li class="glide__slide flex items-center">
					<a
						href={`/${$i18n.language}/proyectos/${project.id}`}
						class="m-auto flex h-2/3 w-fit flex-col items-start gap-y-2 transition-transform hover:scale-110 hover:cursor-pointer"
					>
						<figure class="size-full">
							<img
								src={project.thumbnail.imageUrl}
								alt={project.thumbnail.altText}
								class="h-full"
							/>
							<figcaption>
								<p class="font-Nexa my-5 text-xs font-extralight" style="letter-spacing: 0.1rem;">
									{project.name}
								</p>
							</figcaption>
						</figure>
					</a>
				</li>
			{/each}
		</ul>
		<div
			data-glide-el="controls"
			class="pointer-events-none flex items-center justify-end px-20 text-xl"
		>
			<button
				data-glide-dir=">"
				class="font-Nexa hover:scale-120 pointer-events-auto cursor-pointer transition-transform"
			>
				<img src={logoWhite} alt="Vector: Interior Design" class="h-10" />
			</button>
		</div>
	</div>
</div>

<style>
	#arrow {
		position: absolute;
		left: 50%;
		opacity: 0;
		bottom: 10%;
		transform: translate(-50%, 0) rotate(45deg);
		height: 20px;
		width: 20px;
		border-bottom: 5px solid white;
		border-right: 5px solid white;
		border-radius: 2px;
		transition: all 2s ease-out;
	}

	:global #arrow.showing {
		opacity: 1;
		bottom: 5%;
	}

	:global #arrow.hiding {
		transition: opacity 0.1s;
		opacity: 0;
	}

	:global #arrow.animate {
		animation-name: arrowHover;
		animation-duration: 1s;
		animation-direction: alternate;
		animation-iteration-count: infinite;
	}

	@keyframes arrowHover {
		from {
			bottom: 5%;
		}
		to {
			bottom: 3%;
		}
	}
</style>
