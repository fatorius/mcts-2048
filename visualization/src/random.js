export function getNRandomUniqueNumbers(n, limit) {
    if (n > limit + 1) {
        return []
    }

    const numbers = Array.from({ length: limit + 1 }, (_, i) => i);
    const shuffled = numbers.sort(() => Math.random() - 0.5);
    return shuffled.slice(0, n);
}

export function getRandomFromArray(arr) {
    if (arr.length === 0) {
        return -1;
    }

    return arr[Math.floor(Math.random() * arr.length)];
}

export function getRandomFromArrayWithWeights(arr, weights) {
    if (arr.length === 0 || weights.length === 0 || arr.length !== weights.length) {
        return -1;
    }

    const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
    const normalizedWeights = weights.map(weight => weight / totalWeight);

    const random = Math.random();

    let cumulative = 0;
    for (let i = 0; i < normalizedWeights.length; i++) {
        cumulative += normalizedWeights[i];
        if (random <= cumulative) {
            return arr[i];
        }
    }
}