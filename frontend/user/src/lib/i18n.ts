import i18next from "i18next";
import { createI18nStore } from "svelte-i18next";
import type { i18n } from "i18next";
import { type Writable } from "svelte/store";
import { setContext, getContext } from "svelte";



export const setupI18n = async (lang: 'en' | 'es'): Promise<Writable<i18n>> => {
    await i18next.init({
        lng: lang,
        fallbackLng: 'en',
        resources: {
            en: {
                translation: {
                    "english": "English",
                    'Spanish': 'Spanish',
                    'mainPageMsg': "From sublime to majestic, the limit of this designer is infinite. Defining his client's personality he's capable of converting the most simple of spaces to unique and exclusive works, achieving an accurate and sometimes inimaginable visual aspect.",
                    'sculptures': 'Sculptures',
                    'projects': 'Projects',
                    'sculptureHeader': 'Unique and exclusive works',
                    'conclusionHeader': `Tracing lines with direction, passion, and style.`,
                    'conclusionBody': '**Lines** as a starting and essential element of every design must be focused\n on a direction molding a frame of reference, the **passion** for transforming and\n decorating spaces must always aim for quality and confort, considering\n a set of characteristics that help define a **style** to guarantee in this way\n exclusivity in the project.',
                    'slogan': 'Being different has its advantages',
                    'area': 'Area',
                    'areaUnits': 'square meters'
                }
            },
            es: {
                translation: {
                    'english': "Ingles",
                    'Spanish': 'Español',
                    'mainPageMsg': 'De lo sublime a lo majestuoso, el límite de este  este diseñador es infinito. Definiendo la personalidad de sus clientes es capaz de convertir los espacios más simples en obras únicas y exclusivas, logrando un impacto visual certero e inimaginable.',
                    'sculptures': 'Esculturas',
                    'projects': 'Proyectos',
                    'sculptureHeader': 'Obras únicas y exclusivas',
                    'conclusionHeader': 'Trazando líneas con dirección, pasión y estilo.',
                    'conclusionBody': `Las **líneas** como elemento inicial y esencial de todo diseño deben estar enfocadas\n en una dirección moldeando un marco de referencia, la **pasión** por transformar y\ndecorar los espacios siempre debe apuntar a la calidad y el confort, considerando\nun conjunto de características que ayuden a definir un **estilo** para garantizar de\nesta manera exclusividad en el proyecto.`,
                    'area': 'Área',
                    'areaUnits': 'metros cuadrados'
                }
            }
        },
        interpolation: {
            escapeValue: false, // not needed for svelte as it escapes by default
        }
    });

    return createI18nStore(i18next);
};

const key = 'i18n';


export function setI18n(ctx: Writable<i18n>) { setContext(key, ctx); }
export const getI18n = (): Writable<i18n> => getContext(key);
