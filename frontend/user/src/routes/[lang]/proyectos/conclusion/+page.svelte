<script lang="ts">
	import Head from '$lib/components/Head.svelte';
	import { websiteUrl } from '$lib/utilities/constants';
	import logo from '$lib/images/logo.svg';
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';
	import symbol from '$lib/images/symbol.svg';
	import whiteLogo from '$lib/images/logo white.svg';
	import mdToHtml from '$lib/utilities/markdown';

	const i18n = getI18n();
</script>

<Head
	title={$i18n.language === 'es' ? 'Conclusión' : 'Conclusion'}
	description={$i18n.t('conclusionBody')}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en/proyectos/conclusion`}
	alternateEs={`${websiteUrl}/es/proyectos/conclusion`}
	ogTitle={$i18n.language === 'es' ? 'Conclusión' : 'Conclusion'}
	ogDescription={$i18n.t('conclusionBody')}
	imageUrl={logo}
/>

<div class="header-screen bg-vector-grey relative flex items-center justify-center overflow-clip">
	<div class="w-50 left-3/5 absolute -top-24 flex flex-col items-center md:left-1/4 lg:top-0">
		<img src={symbol} alt="V" id="symbol" class="w-full" />
		<div class="bg-vector-orange relative -top-7 h-screen w-px"></div>
	</div>
	<div
		class="font-Nexa relative top-20 flex size-full flex-col items-center justify-center gap-y-10 px-8 md:flex-row md:justify-around md:px-0 lg:relative lg:h-fit lg:justify-evenly"
	>
		<span
			class="text-vector-cream relative self-start text-4xl font-thin italic leading-10 md:-top-[6ch] md:self-center lg:-top-[4ch] lg:self-start lg:justify-self-start [&_br]:hidden"
			id="slogan"
		>
			{@html mdToHtml($i18n.t('slogan'))}
		</span>
		<div
			class="text-vector-cream bg-vector-grey relative z-20 block py-5 text-justify md:bg-transparent md:max-lg:hidden lg:basis-1/3 [&_strong]:text-white"
		>
			{@html mdToHtml($i18n.t('conclusionBody'))}
		</div>
		<a href={`/${$i18n.language}/`} aria-label="home">
			<img src={whiteLogo} alt="Vector: Interior Design" class="block h-10 md:max-lg:hidden" /></a
		>
		<div class="relative hidden basis-1/2 flex-col items-center gap-0 gap-y-10 md:max-lg:block">
			<div
				class="text-vector-cream bg-vector-grey text-justify brightness-50 lg:bg-transparent [&_strong]:text-white"
			>
				{@html mdToHtml($i18n.t('conclusionBody'))}
			</div>
			<img
				src={whiteLogo}
				alt="Vector: Interior Design"
				class="-bottom-30 absolute right-1/2 h-10 translate-x-1/2"
			/>
			<div class="bg-vector-orange absolute -bottom-40 right-0 h-2 w-8"></div>
		</div>
		<div class="bg-vector-orange -bottom-15 right-10 hidden h-2 w-8 lg:absolute lg:block"></div>
	</div>
</div>

<style global>
	:global {
		#slogan p {
			display: flex;
			flex-direction: column;
		}

		#slogan p strong:nth-of-type(2) {
			align-self: end;
			position: relative;
			left: 2ch;
		}

		@media screen and (width <= 64rem) {
			#slogan p strong:nth-last-of-type(2) {
				left: 1ch;
			}
		}

		#slogan p strong:last-of-type {
			position: relative;
			left: 1ch;
		}
	}
</style>
