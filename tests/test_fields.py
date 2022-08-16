#
# Copyright (c) 2022 by QA Cafe.
# All Rights Reserved.
#

import pytest

from cdrouter.filters import CDRouterFilterError, Field as field

class TestFields:
    def test_field(self):
        assert str(field('id', 'bar', 'buz').eq('foo')) == 'id.bar.buz=foo'

        assert str(field('id').eq('foo'))           == 'id=foo'
        assert str(field('id').eq(123))             == 'id=123'
        assert str(field('id').eq(True))            == 'id=true'
        assert str(field('id').eq(False))           == 'id=false'
        assert str(field('id').not_().eq('foo'))    == 'id!=foo'

        assert str(field('id').ne('foo'))           == 'id!=foo'
        assert str(field('id').ne(123))             == 'id!=123'
        assert str(field('id').ne(True))            == 'id!=true'
        assert str(field('id').ne(False))           == 'id!=false'
        assert str(field('id').not_().ne('foo'))    == 'id=foo'

        assert str(field('id').gt('foo'))           == 'id>foo'
        assert str(field('id').gt(123))             == 'id>123'
        assert str(field('id').gt(123))             == 'id>123'
        assert str(field('id').gt(True))            == 'id>true'
        assert str(field('id').gt(False))           == 'id>false'
        assert str(field('id').not_().gt('foo'))    == 'id<=foo'

        assert str(field('id').ge('foo'))           == 'id>=foo'
        assert str(field('id').ge(123))             == 'id>=123'
        assert str(field('id').ge(True))            == 'id>=true'
        assert str(field('id').ge(False))           == 'id>=false'
        assert str(field('id').not_().ge('foo'))    == 'id<foo'

        assert str(field('id').lt('foo'))           == 'id<foo'
        assert str(field('id').lt(123))             == 'id<123'
        assert str(field('id').lt(True))            == 'id<true'
        assert str(field('id').lt(False))           == 'id<false'
        assert str(field('id').not_().lt('foo'))    == 'id>=foo'

        assert str(field('id').le('foo'))           == 'id<=foo'
        assert str(field('id').le(123))             == 'id<=123'
        assert str(field('id').le(True))            == 'id<=true'
        assert str(field('id').le(False))           == 'id<=false'
        assert str(field('id').not_().le('foo'))    == 'id>foo'

        assert str(field('id').match('foo'))        == 'id~foo'
        assert str(field('id').match(123))          == 'id~123'
        assert str(field('id').match(True))         == 'id~true'
        assert str(field('id').match(False))        == 'id~false'
        assert str(field('id').not_().match('foo')) == 'id!~foo'

        assert str(field('id').match('foo', ignorecase=True))        == 'id~*foo'
        assert str(field('id').match(True, ignorecase=True))         == 'id~*true'
        assert str(field('id').match(False, ignorecase=True))        == 'id~*false'
        assert str(field('id').not_().match('foo', ignorecase=True)) == 'id!~*foo'

        assert str(field('id').contains('foo'))                   == 'id@>{foo}'
        assert str(field('id').contains('foo', 'bar', 'buz'))     == 'id@>{foo,bar,buz}'
        assert str(field('id').contains(1, 2, 3))                 == 'id@>{1,2,3}'
        assert str(field('id').contains(*range(1, 4)))            == 'id@>{1,2,3}'
        assert str(field('id').contains(True))                    == 'id@>{true}'
        assert str(field('id').contains(True, False))             == 'id@>{true,false}'
        assert str(field('id').contains(False))                   == 'id@>{false}'
        with pytest.raises(CDRouterFilterError, match='Filter negate operator not set'):
            str(field('id').not_().contains('foo'))

        assert str(field('id').contained_by('foo'))               == 'id<@{foo}'
        assert str(field('id').contained_by('foo', 'bar', 'buz')) == 'id<@{foo,bar,buz}'
        assert str(field('id').contained_by(1, 2, 3))             == 'id<@{1,2,3}'
        assert str(field('id').contained_by(*range(1, 4)))        == 'id<@{1,2,3}'
        assert str(field('id').contained_by(True))                == 'id<@{true}'
        assert str(field('id').contained_by(True, False))         == 'id<@{true,false}'
        assert str(field('id').contained_by(False))               == 'id<@{false}'
        with pytest.raises(CDRouterFilterError, match='Filter negate operator not set'):
            str(field('id').not_().contained_by('foo'))

        assert str(field('id').overlaps('foo'))                   == 'id&&{foo}'
        assert str(field('id').overlaps('foo', 'bar', 'buz'))     == 'id&&{foo,bar,buz}'
        assert str(field('id').overlaps(1, 2, 3))                 == 'id&&{1,2,3}'
        assert str(field('id').overlaps(*range(1, 4)))            == 'id&&{1,2,3}'
        assert str(field('id').overlaps(True))                    == 'id&&{true}'
        assert str(field('id').overlaps(True, False))             == 'id&&{true,false}'
        assert str(field('id').overlaps(False))                   == 'id&&{false}'
        with pytest.raises(CDRouterFilterError, match='Filter negate operator not set'):
            str(field('id').not_().overlaps('foo'))
