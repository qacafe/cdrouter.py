#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.cdrouter import CDRouter, CDRouterError
from cdrouter.filters import Field as field
from cdrouter.users import User

from .utils import my_cdrouter, my_c # pylint: disable=unused-import

class TestUsers:
    def test_list(self, c):
        (users, links) = c.users.list()
        assert links.current == 1
        assert len(users) == 1
        assert users[0].id == 1
        assert users[0].name == 'admin'

        for ii in range(2, 6):
            u = User(
                admin=True,
                name='admin{}'.format(ii),
                password='mypassword',
                password_confirm='mypassword'
            )
            c.users.create(u)

        (users, links) = c.users.list(limit=1)
        assert links.total == 5
        assert links.last == 5

    def test_iter_list(self, c):
        assert len(list(c.users.iter_list(limit=1))) == 1

        for ii in range(2, 6):
            u = User(
                admin=True,
                name='admin{}'.format(ii),
                password='mypassword',
                password_confirm='mypassword'
            )
            c.users.create(u)

        assert len(list(c.users.iter_list(limit=1))) == 5

    def test_get(self, c):
        u = c.users.get(1)
        assert u.name == 'admin'

        u = User(
            admin=True,
            name='admin2',
            description='i am an admin too',
            password='mypassword',
            password_confirm='mypassword'
        )
        u = c.users.create(u)
        u2 = c.users.get(u.id)
        assert u2.id == u.id
        assert u2.admin is True
        assert u2.disabled is False
        assert u2.name == u.name
        assert u2.description == u.description
        assert u2.created is not None
        assert u2.updated is not None
        assert u2.token is not None

        with pytest.raises(CDRouterError, match='no such user'):
            c.users.get(99999)

    def test_get_by_name(self, c):
        u = c.users.get_by_name('admin')
        assert u.id == 1

        with pytest.raises(CDRouterError, match='no such user'):
            c.users.get_by_name('invalid')

    def test_create(self, c):
        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
        )
        with pytest.raises(CDRouterError, match='empty password not allowed'):
            c.users.create(u)

        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u)
        assert u2.id is not None
        assert u2.admin == u.admin
        assert u2.disabled is False
        assert u2.name == u.name
        assert u2.description == u.description
        assert len(u2.token) > 0

        u = User(
            admin=False,
            name='nonadmin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u)
        assert u2.admin == u.admin

        u = User(
            disabled=True,
            name='disableduser',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u)
        assert u2.disabled is True

    def test_edit(self, c):
        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u)

        u = c.users.get_by_name('admin2')
        u.name = 'admin12345'
        u.admin = not u.admin
        u.description = 'foo foo {} bar bar'.format(u.description)
        u2 = c.users.edit(u)
        assert u2.name == u.name
        assert u2.admin == u.admin
        assert u2.description == u.description

    def test_change_password(self, c):
        u = c.users.get_by_name('admin')
        old = 'cdrouter'

        prefs = c.system.get_preferences()
        prefs.automatic_login = False
        c.system.edit_preferences(prefs)

        c2 = CDRouter(c.base, insecure=c.insecure, username=u.name, password=old)
        c2.system.hostname()

        new = 'cdrouter2'
        u2 = c2.users.change_password(u.id, new, old)
        old = new
        assert u2.token != u.token

        c2 = CDRouter(c.base, insecure=c.insecure, username=u.name, password=new)
        c2.system.hostname()

        new = 'cdrouter3'
        u3 = c2.users.change_password(u.id, new, old, change_token=False)
        old = new
        assert u3.token == u2.token

    def test_change_token(self, c):
        u = c.users.get_by_name('admin')

        prefs = c.system.get_preferences()
        prefs.automatic_login = False
        c.system.edit_preferences(prefs)

        c2 = CDRouter(c.base, insecure=c.insecure, token=u.token)
        c2.system.hostname()

        u2 = c2.users.change_token(u.id)
        assert u2.token != u.token

        c2 = CDRouter(c.base, insecure=c.insecure, token=u2.token)
        c2.system.hostname()

    def test_delete(self, c):
        assert len(list(c.users.iter_list())) == 1

        u = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u)

        assert len(list(c.users.iter_list())) == 2

        c.users.delete(u2.id)

        assert len(list(c.users.iter_list())) == 1

        with pytest.raises(CDRouterError, match='no such user'):
            c.users.get(u2.id)

    def test_bulk_copy(self, c):
        u = c.users.get_by_name('admin')

        u2 = User(
            admin=True,
            name='admin2',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u2)

        u3 = User(
            admin=True,
            name='admin3',
            description='im an admin',
            password='mypassword',
            password_confirm='mypassword'
        )
        u3 = c.users.create(u3)

        ids = [u.id, u2.id, u3.id]

        users = c.users.bulk_copy(ids)
        assert len(users) == 3
        assert users[0].name == 'admin (copy 1)'
        assert users[1].name == 'admin2 (copy 1)'
        assert users[2].name == 'admin3 (copy 1)'

    def test_bulk_edit(self, c):
        u2 = User(
            admin=True,
            name='admin2',
            description='im an admin2',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u2)

        u3 = User(
            admin=True,
            name='admin3',
            description='im an admin3',
            password='mypassword',
            password_confirm='mypassword'
        )
        u3 = c.users.create(u3)

        u4 = User(
            admin=True,
            name='admin4',
            description='im an admin4',
            password='mypassword',
            password_confirm='mypassword'
        )
        u4 = c.users.create(u4)

        new='im changed!'
        c.users.bulk_edit(User(description=new), [u2.id, u3.id, u4.id])
        assert c.users.get(u2.id).description == new
        assert c.users.get(u3.id).description == new
        assert c.users.get(u4.id).description == new

        old=new
        new='im changed again!'
        c.users.bulk_edit(User(description=new), filter=[field('id').ge(u3.id)])
        assert c.users.get(u2.id).description == old
        assert c.users.get(u3.id).description == new
        assert c.users.get(u4.id).description == new

    def test_bulk_delete(self, c):
        u2 = User(
            admin=True,
            name='admin2',
            description='im an admin2',
            password='mypassword',
            password_confirm='mypassword'
        )
        u2 = c.users.create(u2)

        u3 = User(
            admin=True,
            name='admin3',
            description='im an admin3',
            password='mypassword',
            password_confirm='mypassword'
        )
        u3 = c.users.create(u3)

        u4 = User(
            admin=True,
            name='admin4',
            description='im an admin4',
            password='mypassword',
            password_confirm='mypassword'
        )
        u4 = c.users.create(u4)

        c.users.bulk_delete([u3.id, u4.id])
        c.users.get(u2.id)
        with pytest.raises(CDRouterError, match='no such user'):
            c.users.get(u3.id)
        with pytest.raises(CDRouterError, match='no such user'):
            c.users.get(u4.id)

        u3 = User(
            admin=True,
            name='admin3',
            description='im an admin3',
            password='mypassword',
            password_confirm='mypassword'
        )
        u3 = c.users.create(u3)

        u4 = User(
            admin=True,
            name='admin4',
            description='im an admin4',
            password='mypassword',
            password_confirm='mypassword'
        )
        u4 = c.users.create(u4)

        c.users.bulk_delete(filter=[field('id').ge(u3.id)])
        c.users.get(u2.id)
        with pytest.raises(CDRouterError, match='no such user'):
            c.users.get(u3.id)
        with pytest.raises(CDRouterError, match='no such user'):
            c.users.get(u4.id)
