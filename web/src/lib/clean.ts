export const clean = (str: string) => {
    return str.replace(/\\"/g, '"')
  }