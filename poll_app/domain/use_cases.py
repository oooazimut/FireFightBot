from .ports import CacheSetter, FacilityRepo, Receiver


class UseCases:
    def __init__(
        self,
        receiver: Receiver,
        cacher: CacheSetter,
        repo: FacilityRepo,
    ) -> None:
        self._receiver = receiver
        self._cacher = cacher
        self._repo = repo

    def polling(self):
        data = self._receiver.receive()
        self._cacher.set(data)
        self._repo.add(data)
