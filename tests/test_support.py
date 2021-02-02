'''Supports meta functionalities of http-request-codegen.'''

from http_request_codegen import supported_features, supported_methods
from http_request_codegen.hrc_factory import (
    DEFAULT_IMPLEMENTATION,
    DEFAULT_LANGUAGE,
)
from http_request_codegen.hrc_http import HTTP_METHODS


def test_supported_features():
    _default_lang_found, _default_impl_found = (False, False)

    supp_feats = supported_features()
    assert supp_feats
    assert isinstance(supp_feats, dict)

    for lang_or_platform, impls in supp_feats.items():
        assert lang_or_platform
        assert isinstance(lang_or_platform, str)

        if lang_or_platform == DEFAULT_LANGUAGE:
            _default_lang_found = True

        assert impls
        assert isinstance(impls, dict)

        for impl_name, meth_feats in impls.items():
            assert impl_name
            assert isinstance(impl_name, str)

            if impl_name == DEFAULT_IMPLEMENTATION:
                _default_impl_found = True

            assert meth_feats
            assert isinstance(meth_feats, dict)

            _at_least_a_feature_for_impl = False

            for method, features in meth_feats.items():
                assert method
                assert isinstance(method, str)
                assert method.isupper()
                assert method in HTTP_METHODS

                assert features
                assert isinstance(features, dict)

                _method_supported = False

                for feature_name, supported in features.items():
                    assert feature_name
                    assert isinstance(feature_name, str)

                    assert isinstance(supported, bool)

                    if supported:
                        _at_least_a_feature_for_impl = True
                        _method_supported = True

                # Special attribute that resumes method support
                assert features['_supported'] == _method_supported

            assert _at_least_a_feature_for_impl

    assert _default_lang_found
    assert _default_impl_found


def test_supported_methods():
    supp_meths = supported_methods()
    assert supp_meths
    assert isinstance(supp_meths, dict)

    for lang_or_platform, impls in supp_meths.items():
        assert lang_or_platform
        assert isinstance(lang_or_platform, str)

        assert impls
        assert isinstance(impls, dict)

        for impl_name, methods in impls.items():
            assert impl_name
            assert isinstance(impl_name, str)

            assert methods  # can't be empty
            assert isinstance(methods, list)
