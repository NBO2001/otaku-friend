

export const generSplit = (genre: String) => {
    return genre.split("|").join(" - ");
}