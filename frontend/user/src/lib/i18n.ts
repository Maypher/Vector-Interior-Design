import i18next from "i18next";
import { createI18nStore } from "svelte-i18next";
import type { i18n } from "i18next";
import { type Writable } from "svelte/store";
import { setContext, getContext } from "svelte";

await i18next.init({
    lng: 'en',
    fallbackLng: 'es',
    resources: {
        en: {
            translation: {
                "english": "English",
                'Spanish': 'Spanish',
                'mainPageMsg': "From sublime to majestic, the limit of this designer is infinite. Defining his client's personality he's capable of converting the most simple of spaces to unique and exclusive works, achieving an accurate and sometimes inimaginable visual aspect.",
                'sculptures': 'Sculptures',
                'projects': 'Projects',
                'sculptureHeader': 'Unique and exclusive works',
                'conclusionMain': `Every project requires a complex design, based on clear and objective guidelines. However, when
creating rules can be broken always maintaining harmony, offering exclusivity and improvements to your quality of life`,
                'conclusionSecondary': 'That is why...',
                'slogan': 'Being different has its advantages',
                'area': 'Area',
                'areaUnits': 'square meters'
            }
        },
        es: {
            translation: {
                'english': "Ingles",
                'Spanish': 'Español',
                'mainPageMsg': 'De lo sublime a lo majestuoso, el límite de este  este diseñador es infinito. Definiendo la personalidad de sus clientes es capaz de convertir los espacios más simples en obras únicas y exclusivas, logrando un impacto visual certero y a veces hasta inimaginable.',
                'sculptures': 'Esculturas',
                'projects': 'Proyectos',
                'sculptureHeader': 'Obras Únicas y Exclusivas',
                'conclusionMain': `Todo proyecto requiere de un diseño complejo, basado en lineamientos claros y objetivos, sin embargo a la hora 
de crear se pueden romper las reglas manteniendo siempre armonía, ofreciendo exclusividad y mejoras en tu calidad de vida.`,
                'conclusionSecondary': 'Es por eso que...',
                'slogan': 'Ser diferente tiene sus ventajas',
                'area': 'Área',
                'areaUnits': 'metros cuadrados'
            }
        }
    },
    interpolation: {
        escapeValue: false, // not needed for svelte as it escapes by default
    }
});

export const setupI18n = () => createI18nStore(i18next);

const key = 'i18n';

export function setI18n(ctx: Writable<i18n>) { setContext(key, ctx); }
export const getI18n = (): Writable<i18n> => getContext(key);
