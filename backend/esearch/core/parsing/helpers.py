from typing import Callable, Generator, List, Tuple, TypeVar

T = TypeVar("T")


def unpack_generator(
    generator: Generator[Tuple[List[T], int], None, None]
) -> Generator[Tuple[T, int], None, None]:
    for item_list, count in generator:
        for item in item_list:
            yield item, count


def get_generator_packer(
    batch_size: int = 128,
) -> Callable[
    [Generator[Tuple[T, int], None, None]], Generator[Tuple[List[T], int], None, None]
]:
    def generator_packer(
        generator: Generator[Tuple[T, int], None, None]
    ) -> Generator[Tuple[List[T], int], None, None]:
        batch: List[T] = []
        current_count = 0
        for item, item_count in generator:
            batch.append(item)
            current_count = item_count
            if len(batch) == batch_size:
                yield batch, item_count
                batch = []
        yield batch, current_count

    return generator_packer
