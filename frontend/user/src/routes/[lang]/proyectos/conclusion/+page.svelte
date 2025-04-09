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

<div
	class="header-screen bg-vector-grey min-h-150 relative flex items-center justify-evenly overflow-clip"
>
	<span
		class="text-vector-cream relative bottom-[12ch] text-xl font-thin italic leading-10 md:bottom-[4ch] md:text-4xl [&_br]:hidden"
		id="slogan"
	>
		{@html mdToHtml($i18n.t('slogan'))}
	</span>

	<div
		class="-top-1/10 right-1/5 absolute flex h-full w-0.5 flex-col items-center overflow-visible md:relative md:right-auto md:ml-4 lg:ml-0"
	>
		<img src={symbol} alt="V" id="symbol" class="relative right-px min-w-52" />
		<div class="bg-vector-orange relative bottom-8 min-h-[200%] min-w-0.5"></div>
	</div>

	<div
		class="text-vector-cream bg-vector-grey relative z-20 hidden py-5 text-justify brightness-50 md:bg-transparent lg:block lg:basis-1/3 [&_strong]:text-white"
	>
		{@html mdToHtml($i18n.t('conclusionBody'))}
	</div>
	<a href={`/${$i18n.language}/`} aria-label="home">
		<img src={whiteLogo} alt="Vector: Interior Design" class="hidden h-10 lg:block" /></a
	>
	<div class="top-1/9 relative flex basis-1/2 flex-col items-center gap-y-10 md:top-auto lg:hidden">
		<div class="bg-vector-grey">
			<div
				class="text-vector-cream text-justify brightness-50 lg:bg-transparent [&_strong]:text-white"
			>
				{@html mdToHtml($i18n.t('conclusionBody'))}
			</div>
		</div>
		<img src={whiteLogo} alt="Vector: Interior Design" class="h-10 self-start md:self-center" />
		<div class="bg-vector-orange -bottom-15 absolute right-0 h-2 w-8"></div>
	</div>
	<div class="bg-vector-orange -bottom-15 right-10 hidden h-2 w-8 lg:absolute lg:block"></div>
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
