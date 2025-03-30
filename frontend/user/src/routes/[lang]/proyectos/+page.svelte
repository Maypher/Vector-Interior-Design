<script lang="ts">
	import { websiteUrl } from '$lib/utilities/constants';
	import Head from '$lib/components/Head.svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';
	import Glide, { Controls, Swipe } from '@glidejs/glide/dist/glide.modular.esm.js';
	import '@glidejs/glide/dist/css/glide.core.min.css';
	import ProjectSkeleton from '$lib/components/ProjectSkeleton.svelte';

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
	ogDescription={$i18n.language === 'es' ? 'Proyectos' : 'Projects'}
	imageUrl={projects.at(0).thumbnail.imageUrl}
/>

<ul class="header-screen bg-vector-grey snap-y snap-mandatory overflow-y-scroll lg:hidden">
	{#each projects as project, i (project.id)}
		{#if project.thumbnail}
			<li class="flex h-full snap-center items-center justify-center text-white" id={project.id}>
				<ProjectSkeleton
					id={project.id}
					imageUrl={project.thumbnail?.imageUrl}
					imageAltText={project.thumbnail.altText}
					projectName={project.name}
				/>
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
			{#each projects as project (project.id)}
				<li class="glide__slide flex items-center">
					<ProjectSkeleton
						id={project.id}
						imageUrl={project.thumbnail?.imageUrl}
						imageAltText={project.thumbnail.altText}
						projectName={project.name}
					/>
				</li>
			{/each}
		</ul>
		<div
			data-glide-el="controls"
			class="pointer-events-none flex items-center justify-end gap-x-5 px-20 text-xl"
		>
			<button
				data-glide-dir="<"
				class="font-Nexa hover:scale-120 pointer-events-auto cursor-pointer transition-transform"
				aria-label={$i18n.language === 'es' ? 'Anterior' : 'Previous'}
			>
				<div class="font-Nexa gradient-background text-vector-cream h-fit text-6xl font-extrabold">
					<div id="carouselArrow">&lt;</div>
				</div>
			</button>
			<button
				data-glide-dir=">"
				class="font-Nexa hover:scale-120 pointer-events-auto cursor-pointer transition-transform"
				aria-label={$i18n.language === 'es' ? 'Siguiente' : 'Next'}
			>
				<div class="font-Nexa gradient-background text-vector-cream h-fit text-6xl font-extrabold">
					<div id="carouselArrow">&gt;</div>
				</div>
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
	/* 
	#carouselArrow {
		animation: 1s ease-in-out infinite both alternate move-arrow;
	} */

	@keyframes move-arrow {
		to {
			transform: translateX(1rem);
		}
	}
</style>
