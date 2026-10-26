from fastapi import APIRouter, Header, Request, Response

from ..identity import IdentityError
from ..identity_schemas import (Bootstrap, BootstrapResult, IdentityResult, ProfileCreate,
                                ProfileList, ProfileResult, ProfileSelect, IdentityAction, ProfileDelete, ProfileEdit)
from ..repositories import identities


def router(path):
    api = APIRouter(prefix='/api')

    @api.post('/identity/bootstrap', response_model=BootstrapResult, status_code=201)
    def bootstrap(body: Bootstrap, request: Request, response: Response):
        origin = request.headers.get('origin')
        if origin and origin not in {'http://127.0.0.1:5173', 'http://localhost:5173',
                                     'http://127.0.0.1:8000', 'http://localhost:8000'}:
            raise IdentityError(403, 'origin_not_allowed', 'Open the local coursework application.')
        response.headers['Cache-Control'] = 'no-store'
        return identities.bootstrap(path, body)

    @api.get('/identity', response_model=IdentityResult)
    def identity(authorization: str | None = Header(None)):
        return identities.read_identity(path, authorization)

    @api.get('/profiles', response_model=ProfileList)
    def listing(authorization: str | None = Header(None)):
        return identities.listing(path, authorization)

    @api.post('/profiles', response_model=ProfileResult, status_code=201)
    def create(body: ProfileCreate, response: Response, authorization: str | None = Header(None)):
        result = identities.create(path, authorization, body)
        response.status_code = 200 if result['replayed'] else 201
        return result

    @api.post('/identity/select', response_model=IdentityResult)
    def select(body: ProfileSelect, authorization: str | None = Header(None)):
        return identities.select(path, authorization, body)

    @api.get('/profile', response_model=ProfileResult)
    def read(authorization: str | None = Header(None)):
        return identities.read_profile(path, authorization)

    @api.post('/identity/guest', response_model=IdentityResult)
    def guest(body: IdentityAction, authorization: str | None = Header(None)):
        return identities.guest(path, authorization, body)

    @api.post('/identity/leave', response_model=IdentityResult)
    def leave(body: IdentityAction, authorization: str | None = Header(None)):
        return identities.leave(path, authorization, body)

    @api.post('/profile/delete', response_model=IdentityResult)
    def delete(body: ProfileDelete, authorization: str | None = Header(None)):
        return identities.leave(path, authorization, body, delete=True)

    @api.patch('/profile', response_model=ProfileResult)
    def edit(body: ProfileEdit, authorization: str | None = Header(None)):
        return identities.edit(path, authorization, body)

    return api
