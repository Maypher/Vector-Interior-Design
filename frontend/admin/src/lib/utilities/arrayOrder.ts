/**
 * Used for values that can be reordered. Get's the difference between the original order and new order
 * to only update the values that changed.
 * @param oldList The original order of the data in an array of its unique ids.
 * @param newList The new order of the data in an array of its unique ids.
 * @returns A list with only the updated indexes in the form {id, newPos}
 */
export default function getArrayDifference(oldList: string[], newList: string[]): { id: string, newPos: number }[] {
    let differences: { id: string; newPos: number }[] = [];

    newList.forEach((item, i) => {
        const originalIndex = oldList.indexOf(item);
        if (originalIndex !== i) {
            differences.push({ id: item, newPos: i });
        }
    });

    return differences;
}
