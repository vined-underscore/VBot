from typing import Any, AsyncGenerator, Sequence, Tuple
import math


class AsyncPaginator:
    """An asynchronous paginator for a given iterable.

    Parameters
    -----------
    iterable: Sequence[:class:`Any`]
        The iterable to paginate.

    page_size: :class:`int`
        The number of items to include in each page.
    """

    def __init__(self, iterable: Sequence[Any], page_size: int = 5) -> None:
        self.iterable: Sequence[Any] = iterable
        self.page_size: int = page_size
        self.num_pages: int = -1

    async def count(self) -> int:
        """Returns the total number of pages in the iterable.

        Returns
        -------
        int
            The count of pages.
        """

        if self.num_pages == -1:
            self.num_pages = math.ceil(len(self.iterable) / self.page_size)
        return self.num_pages

    async def get_page(self, page_num: int) -> Sequence[Any]:
        """Returns a list of items for the specified page number.

        Parameters
        ----------
        page_num: int
            The page number to retrieve.

        Returns
        -------
        Sequence[:class:`Any`]
            The page at the index.
        """

        index_range: Tuple[int, int] = (page_num - 1) * self.page_size, page_num * self.page_size
        page_data: Sequence[Any] = self.iterable[slice(*index_range)]
        return page_data

    async def iterate_pages(self) -> AsyncGenerator[Sequence[Any], None]:
        """Iterates over all pages of the iterable asynchronously, yielding a list of items for each page.

        Returns
        -------
        AsyncGenerator[Sequence[:class:`Any`], None]
            An async generator with all of the pages.
        """

        async with self.count() as count:
            for page_num in range(1, count + 1):
                yield await self.get_page(page_num)

    async def __aiter__(self) -> AsyncGenerator[Sequence[Any], None]:
        """Allows for intuitive iteration over pages using async for.

        Returns
        -------
        AsyncGenerator[Sequence[:class:`Any`], None]
            An async generator with all of the pages.
        """

        async for page in self.iterate_pages():
            yield page